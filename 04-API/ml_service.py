"""ML Service — loads RandomForest models and extracts decision tree paths."""
import json
import pickle
import numpy as np
from pathlib import Path

ROOT = Path(__file__).parent.parent
ACTIVE_MODEL_FILE = Path(__file__).parent / "active_model.txt"

FEATURE_LABELS = {
    "n1_norm":           "N1 (1º Bimestre)",
    "n2_norm":           "N2 (2º Bimestre)",
    "n3_norm":           "N3 (3º Bimestre)",
    "n4_norm":           "N4 (4º Bimestre)",
    "slope_notas":       "Tendência (N1→N4)",
    "variancia_notas":   "Variância das notas",
    "media_geral_aluno": "Média geral do aluno",
    "serie_num_norm":    "Série escolar",
    "media_turma_norm":  "Média da turma",
}

CLASS_NAMES  = {0: "Reprovado", 1: "Recuperação", 2: "Aprovado"}
CLASS_COLORS = {0: "#EF4444", 1: "#F59E0B", 2: "#10B981"}

ALL_MODELS = ["RF_M1", "RF_M2", "RF_M3"]


class MLService:
    _instance: "MLService | None" = None

    def __init__(self):
        self.models:   dict = {}   # name → sklearn clf
        self.metadata: dict = {}   # name → dict (loaded for ALL models)
        self._active:  str  = "RF_M3"
        self._models_dir    = self._find_models_dir()
        self._load_all_metadata()
        self._load_active()

    # ── singleton ────────────────────────────────────────────────────────────
    @classmethod
    def get(cls) -> "MLService":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    # ── internals ────────────────────────────────────────────────────────────
    def _find_models_dir(self) -> Path:
        dirs = [ROOT / "ml_models", ROOT / "02-ML" / "ml_models"]
        return next((d for d in dirs if d.exists()), dirs[0])

    def _load_all_metadata(self):
        """Load JSON metadata for every model (even unloaded ones)."""
        fallback = ROOT / "02-ML" / "ml_models"
        for name in ALL_MODELS:
            for d in [self._models_dir, fallback]:
                meta = d / f"{name}_metadata.json"
                if meta.exists():
                    try:
                        self.metadata[name] = json.loads(meta.read_text(encoding="utf-8"))
                    except Exception:
                        pass
                    break

    def _load_active(self):
        """Load the active model from disk (reads active_model.txt if exists)."""
        if ACTIVE_MODEL_FILE.exists():
            name = ACTIVE_MODEL_FILE.read_text().strip()
            if name in ALL_MODELS:
                self._active = name
        self.load_model(self._active)

    def load_model(self, name: str) -> bool:
        """Load a specific model pickle into memory."""
        if name in self.models:
            return True
        pkl = self._models_dir / f"{name}.pkl"
        if not pkl.exists():
            # try fallback dir
            fallback = ROOT / "02-ML" / "ml_models" / f"{name}.pkl"
            if fallback.exists():
                pkl = fallback
            else:
                print(f"[ML] {name}.pkl não encontrado")
                return False
        try:
            with open(pkl, "rb") as f:
                self.models[name] = pickle.load(f)
            acc = self.metadata.get(name, {}).get("accuracy", 0)
            print(f"[ML] {name} carregado — acurácia: {acc:.1%}")
            return True
        except Exception as e:
            print(f"[ML] Falha em {name}: {e}")
            return False

    def unload_others(self, keep: str):
        """Remove all models from memory except `keep`."""
        for name in list(self.models.keys()):
            if name != keep:
                del self.models[name]
                print(f"[ML] {name} descarregado da memória")

    def activate(self, name: str) -> bool:
        """Load `name`, unload others, persist choice to disk."""
        if name not in ALL_MODELS:
            return False
        ok = self.load_model(name)
        if ok:
            self._active = name
            self.unload_others(name)
            ACTIVE_MODEL_FILE.write_text(name)
        return ok

    # ── public API ───────────────────────────────────────────────────────────
    def is_available(self, name: str) -> bool:
        return name in self.models

    @property
    def active(self) -> str:
        return self._active

    def list_models(self) -> list:
        """Return info for ALL 3 models — loaded or not — so the UI can show all cards."""
        result = []
        for name in ALL_MODELS:
            result.append({
                "name":       name,
                "accuracy":   self.metadata.get(name, {}).get("accuracy", 0),
                "n_features": self.metadata.get(name, {}).get("n_features", 0),
                "features":   self.metadata.get(name, {}).get("features", []),
                "available":  name in self.models,
                "active":     name == self._active,
            })
        return result

    def predict_ensemble(self, model_name: str, feature_vector: list) -> dict:
        """Predict using all trees; return class, proba, and per-tree vote counts."""
        if model_name not in self.models:
            # Auto-load if needed (graceful fallback)
            if not self.load_model(model_name):
                return None
        rf = self.models[model_name]
        feature_names = self.metadata.get(model_name, {}).get("features", [])

        X_np = np.array([feature_vector])
        if feature_names and len(feature_names) == len(feature_vector):
            import pandas as pd
            X = pd.DataFrame([feature_vector], columns=feature_names)
        else:
            X = X_np

        proba = rf.predict_proba(X)[0].tolist()
        pred = int(np.argmax(proba))

        votes = [0, 0, 0]
        for est in rf.estimators_:
            p = int(est.predict(X_np)[0])
            if 0 <= p < 3:
                votes[p] += 1

        return {
            "class_value": pred,
            "class_name":  CLASS_NAMES.get(pred, str(pred)),
            "class_color": CLASS_COLORS.get(pred, "#64748B"),
            "proba":       [round(p, 3) for p in proba],
            "confidence":  round(max(proba), 3),
            "votes":       votes,
            "n_trees":     len(rf.estimators_),
        }

    def extract_decision_path(
        self,
        model_name: str,
        feature_vector: list,
        tree_idx: int = 0,
        max_depth_off_path: int = 6,
    ) -> dict | None:
        from sklearn.tree._tree import TREE_LEAF

        if model_name not in self.models:
            if not self.load_model(model_name):
                return None

        rf = self.models[model_name]
        feature_names = self.metadata.get(model_name, {}).get("features", [])

        X = np.array([feature_vector], dtype=np.float64)
        estimator = rf.estimators_[tree_idx % len(rf.estimators_)]
        tree_ = estimator.tree_

        indicator = estimator.decision_path(X)
        path_ids: set[int] = {int(i) for i in indicator.indices}
        leaf_node_id = int(indicator.indices[-1])

        def make_node(node_id: int, depth: int = 0) -> dict:
            is_leaf = bool(tree_.feature[node_id] == TREE_LEAF)
            values = tree_.value[node_id][0].tolist()
            total = sum(values) or 1.0
            majority = int(np.argmax(values))
            on_path = bool(node_id in path_ids)

            node: dict = {
                "id":            node_id,
                "on_path":       on_path,
                "is_leaf":       is_leaf,
                "samples":       int(tree_.n_node_samples[node_id]),
                "class_dist":    [int(v) for v in values],
                "class_proba":   [round(v / total, 3) for v in values],
                "majority_class": majority,
                "majority_name": CLASS_NAMES.get(majority, str(majority)),
                "majority_color": CLASS_COLORS.get(majority, "#64748B"),
                "depth":         depth,
                "impurity":      round(float(tree_.impurity[node_id]), 4),
            }

            if not is_leaf:
                feat_idx  = int(tree_.feature[node_id])
                threshold = float(tree_.threshold[node_id])
                feat_name = feature_names[feat_idx] if 0 <= feat_idx < len(feature_names) else f"x{feat_idx}"
                student_val = float(X[0, feat_idx]) if 0 <= feat_idx < X.shape[1] else 0.0

                node.update({
                    "feature":       feat_name,
                    "feature_label": FEATURE_LABELS.get(feat_name, feat_name),
                    "threshold":     round(threshold, 4),
                    "student_value": round(student_val, 4),
                    "goes_left":     bool(student_val <= threshold),
                })

                left_id  = int(tree_.children_left[node_id])
                right_id = int(tree_.children_right[node_id])

                children = []
                for child_id in [left_id, right_id]:
                    child_on_path = child_id in path_ids
                    if child_on_path or (on_path and depth < max_depth_off_path):
                        children.append(make_node(child_id, depth + 1))
                if children:
                    node["children"] = children

            return node

        tree_data = make_node(0)

        leaf_values = tree_.value[leaf_node_id][0].tolist()
        leaf_total  = sum(leaf_values) or 1.0
        leaf_proba  = [v / leaf_total for v in leaf_values]
        pred_class  = int(np.argmax(leaf_proba))

        return {
            "tree":        tree_data,
            "path_ids":    sorted(path_ids),
            "leaf_id":     leaf_node_id,
            "path_length": len(path_ids),
            "prediction": {
                "class_value": pred_class,
                "class_name":  CLASS_NAMES.get(pred_class, str(pred_class)),
                "class_color": CLASS_COLORS.get(pred_class, "#64748B"),
                "proba":       [round(p, 3) for p in leaf_proba],
                "confidence":  round(max(leaf_proba), 3),
            },
        }

    def get_ensemble_votes_sequence(
        self, model_name: str, feature_vector: list
    ) -> list[int]:
        """Return the class predicted by each individual estimator (for timelapse)."""
        if model_name not in self.models:
            if not self.load_model(model_name):
                return []
        rf = self.models[model_name]
        X = np.array([feature_vector], dtype=np.float64)
        return [int(est.predict(X)[0]) for est in rf.estimators_]
