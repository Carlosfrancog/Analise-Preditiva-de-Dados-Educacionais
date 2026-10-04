"""Endpoints da pipeline temporal usada no artigo."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from research.services.research_service import ResearchService, ResearchServiceError


router = APIRouter(tags=["research"])
service = ResearchService()


class ResearchPredictionRequest(BaseModel):
    cutoff: str = Field(description="Corte temporal: M1, M2 ou M3")
    features: dict[str, float] = Field(
        description="Valores das features do snapshot selecionado"
    )


def _domain_error(error: ResearchServiceError) -> HTTPException:
    message = str(error)
    status = 503 if "execute research.run_initial_pipeline" in message else 400
    return HTTPException(status_code=status, detail=message)


@router.get("/research/status")
def research_status() -> dict[str, Any]:
    """Informa se snapshots e modelos necessários para a interface existem."""
    try:
        catalog = service.catalog()
    except ResearchServiceError as error:
        raise _domain_error(error) from error
    return {
        "status": (
            "ready"
            if all(item["rows"] > 0 and item["model_available"] for item in catalog)
            else "not_ready"
        ),
        "pipeline": "research-rf-v1",
        "snapshots": catalog,
    }


@router.get("/research/snapshots")
def research_snapshots() -> list[dict[str, Any]]:
    try:
        return service.catalog()
    except ResearchServiceError as error:
        raise _domain_error(error) from error


@router.get("/research/snapshots/{cutoff}/samples")
def research_samples(
    cutoff: str,
    limit: int = Query(default=25, ge=1, le=200),
    student_id: str | None = None,
    academic_year: int | None = None,
    include_prediction: bool = True,
) -> list[dict[str, Any]]:
    try:
        return service.samples(
            cutoff,
            limit=limit,
            student_id=student_id,
            academic_year=academic_year,
            include_prediction=include_prediction,
        )
    except (ResearchServiceError, FileNotFoundError) as error:
        raise _domain_error(ResearchServiceError(str(error))) from error


@router.post("/research/predict")
def research_predict(payload: ResearchPredictionRequest) -> dict[str, Any]:
    try:
        return service.predict_features(payload.cutoff, payload.features)
    except (ResearchServiceError, FileNotFoundError) as error:
        raise _domain_error(ResearchServiceError(str(error))) from error
