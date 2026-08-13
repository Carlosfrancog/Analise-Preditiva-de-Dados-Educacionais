"""Importar dados via CSV com validação."""
import io, csv
from fastapi import APIRouter, UploadFile, File, HTTPException
import cads

router = APIRouter(tags=["importar"])

REQUIRED_ALUNOS = {"nome", "sala_codigo"}
REQUIRED_NOTAS  = {"matricula", "materia", "n1"}


def _read_csv(content: bytes) -> list[dict]:
    text = content.decode("utf-8-sig").strip()
    reader = csv.DictReader(io.StringIO(text))
    return list(reader)


@router.get("/importar/templates")
def get_templates():
    return {
        "alunos": {
            "colunas":   ["nome", "sala_codigo"],
            "exemplo":   [
                {"nome": "João Silva", "sala_codigo": "6FA"},
                {"nome": "Maria Santos", "sala_codigo": "7FB"},
            ],
            "descricao": "Importa novos alunos. sala_codigo deve ser o código de uma turma existente.",
        },
        "notas": {
            "colunas":   ["matricula", "materia", "n1", "n2", "n3", "n4"],
            "exemplo":   [
                {"matricula": "6FA0001", "materia": "Matemática", "n1": "7.5", "n2": "8.0", "n3": "6.5", "n4": "7.0"},
                {"matricula": "6FA0001", "materia": "Português",  "n1": "8.0", "n2": "7.5", "n3": "9.0", "n4": ""},
            ],
            "descricao": "Importa ou atualiza notas. Campos n2/n3/n4 são opcionais (ano em aberto).",
        },
    }


@router.post("/importar/preview/alunos")
async def preview_alunos(file: UploadFile = File(...)):
    content = await file.read()
    try:
        rows = _read_csv(content)
    except Exception as e:
        raise HTTPException(400, f"Erro ao ler CSV: {e}")

    if not rows:
        raise HTTPException(400, "Arquivo vazio.")

    cols = set(rows[0].keys())
    missing = REQUIRED_ALUNOS - cols
    if missing:
        raise HTTPException(400, f"Colunas obrigatórias ausentes: {missing}")

    conn = cads.get_conn()
    salas_db = {r["codigo"]: r["id"] for r in conn.execute("SELECT id, codigo FROM salas").fetchall()}
    conn.close()

    ok, errors = [], []
    for i, row in enumerate(rows, 1):
        nome = row.get("nome", "").strip()
        codigo = row.get("sala_codigo", "").strip().upper()
        if not nome:
            errors.append({"linha": i, "erro": "Nome vazio", "row": row})
        elif codigo not in salas_db:
            errors.append({"linha": i, "erro": f"Turma '{codigo}' não existe", "row": row})
        else:
            ok.append({"nome": nome, "sala_codigo": codigo, "sala_id": salas_db[codigo]})

    return {"total": len(rows), "validos": len(ok), "erros": len(errors), "preview": ok[:10], "detalhes_erros": errors[:20]}


@router.post("/importar/executar/alunos")
async def executar_alunos(file: UploadFile = File(...)):
    content = await file.read()
    rows = _read_csv(content)

    conn = cads.get_conn()
    salas_db = {r["codigo"]: r["id"] for r in conn.execute("SELECT id, codigo FROM salas").fetchall()}

    inseridos, ignorados = 0, 0
    for row in rows:
        nome = row.get("nome", "").strip()
        codigo = row.get("sala_codigo", "").strip().upper()
        if not nome or codigo not in salas_db:
            ignorados += 1
            continue
        sala_id = salas_db[codigo]
        matricula = cads.gerar_matricula(sala_id)
        try:
            conn.execute("INSERT INTO alunos (nome, sala_id, matricula) VALUES (?,?,?)",
                         (nome, sala_id, matricula))
            inseridos += 1
        except Exception:
            ignorados += 1

    conn.commit()
    conn.close()
    return {"inseridos": inseridos, "ignorados": ignorados}


@router.post("/importar/preview/notas")
async def preview_notas(file: UploadFile = File(...)):
    content = await file.read()
    try:
        rows = _read_csv(content)
    except Exception as e:
        raise HTTPException(400, f"Erro ao ler CSV: {e}")

    if not rows:
        raise HTTPException(400, "Arquivo vazio.")

    cols = set(rows[0].keys())
    missing = REQUIRED_NOTAS - cols
    if missing:
        raise HTTPException(400, f"Colunas obrigatórias ausentes: {missing}")

    conn = cads.get_conn()
    matriculas = {r["matricula"]: r["id"] for r in conn.execute("SELECT id, matricula FROM alunos").fetchall()}
    materias   = {r["nome"].lower(): r["id"] for r in conn.execute("SELECT id, nome FROM materias").fetchall()}
    conn.close()

    ok, errors = [], []
    for i, row in enumerate(rows, 1):
        mat  = row.get("matricula", "").strip()
        disc = row.get("materia", "").strip()

        if mat not in matriculas:
            errors.append({"linha": i, "erro": f"Matrícula '{mat}' não encontrada", "row": row})
            continue
        if disc.lower() not in materias:
            errors.append({"linha": i, "erro": f"Matéria '{disc}' não encontrada", "row": row})
            continue

        notas_vals = {}
        nota_error = None
        for k in ("n1", "n2", "n3", "n4"):
            v = row.get(k, "").strip()
            if not v:
                notas_vals[k] = None
            else:
                try:
                    fv = float(v)
                    if not 0 <= fv <= 10:
                        nota_error = f"{k}={v} fora do intervalo 0-10"
                        break
                    notas_vals[k] = round(fv, 1)
                except ValueError:
                    nota_error = f"{k}='{v}' não é um número"
                    break

        if nota_error:
            errors.append({"linha": i, "erro": nota_error, "row": row})
        else:
            ok.append({"matricula": mat, "materia": disc, **notas_vals,
                       "aluno_id": matriculas[mat], "materia_id": materias[disc.lower()]})

    return {"total": len(rows), "validos": len(ok), "erros": len(errors), "preview": ok[:10], "detalhes_erros": errors[:20]}


@router.post("/importar/executar/notas")
async def executar_notas(file: UploadFile = File(...)):
    content = await file.read()
    rows = _read_csv(content)

    conn = cads.get_conn()
    matriculas = {r["matricula"]: r["id"] for r in conn.execute("SELECT id, matricula FROM alunos").fetchall()}
    materias   = {r["nome"].lower(): r["id"] for r in conn.execute("SELECT id, nome FROM materias").fetchall()}

    inseridos = atualizados = ignorados = 0
    for row in rows:
        mat  = row.get("matricula", "").strip()
        disc = row.get("materia", "").strip()
        if mat not in matriculas or disc.lower() not in materias:
            ignorados += 1
            continue

        aluno_id   = matriculas[mat]
        materia_id = materias[disc.lower()]
        notas = {}
        for k in ("n1", "n2", "n3", "n4"):
            v = row.get(k, "").strip()
            notas[k] = float(v) if v else None

        existing = conn.execute(
            "SELECT id FROM notas WHERE aluno_id=? AND materia_id=?", (aluno_id, materia_id)
        ).fetchone()
        if existing:
            conn.execute(
                "UPDATE notas SET n1=?,n2=?,n3=?,n4=? WHERE aluno_id=? AND materia_id=?",
                (notas["n1"], notas["n2"], notas["n3"], notas["n4"], aluno_id, materia_id),
            )
            atualizados += 1
        else:
            conn.execute(
                "INSERT INTO notas (aluno_id, materia_id, n1, n2, n3, n4) VALUES (?,?,?,?,?,?)",
                (aluno_id, materia_id, notas["n1"], notas["n2"], notas["n3"], notas["n4"]),
            )
            inseridos += 1

    conn.commit()
    conn.close()
    return {"inseridos": inseridos, "atualizados": atualizados, "ignorados": ignorados}
