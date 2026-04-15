#!/usr/bin/env python3
"""
Debug de tipos de dados
"""

import numpy as np
from ml_pipeline import train_random_forest
import json

model, results, mapping = train_random_forest(model_type='M1', verbose=False)

def check_types(obj, prefix=""):
    """Verifica tipos recursivamente."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            print(f"{prefix}{k}: {type(v).__name__}")
            if isinstance(v, (dict, list)):
                check_types(v, prefix + "  ")
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            print(f"{prefix}[{i}]: {type(v).__name__}")
            if isinstance(v, (dict, list)) and len(str(v)) < 100:
                check_types(v, prefix + "  ")

print("Results:")
check_types(results)

print("\n\nMapping:")
check_types(mapping)

# Tentar serializar
def serialize(obj):
    if obj is None:
        return None
    if isinstance(obj, bool):
        return obj
    if isinstance(obj, (int, float)):
        return obj
    if isinstance(obj, np.bool_):
        return bool(obj)
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        return float(obj)
    if isinstance(obj, np.ndarray):
        return serialize(obj.tolist())
    if isinstance(obj, dict):
        return {k: serialize(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [serialize(i) for i in obj]
    if isinstance(obj, (str, bytes)):
        return obj
    return str(obj)

try:
    serialized = serialize(results)
    print("\n\n✅ Serialização bem-sucedida!")
except Exception as e:
    print(f"\n\n❌ Erro na serialização: {e}")
    import traceback
    traceback.print_exc()
