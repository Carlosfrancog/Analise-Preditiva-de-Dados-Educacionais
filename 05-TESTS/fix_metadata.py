#!/usr/bin/env python3
"""
🔧 Corrige metadata.json dos modelos treinados
"""

import json
import ast
from pathlib import Path

models_dir = Path("ml_models")

for model_dir in models_dir.glob("RF_M*"):
    metadata_file = model_dir / "metadata.json"
    
    if not metadata_file.exists():
        continue
    
    print(f"🔧 Corrigindo {model_dir.name}...")
    
    try:
        # Ler conteúdo
        with open(metadata_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        print(f"   Conteúdo lido (primeiros 100 caracteres): {content[:100]}")
        
        # Tentar json.loads primeiro
        try:
            data = json.loads(content)
            print(f"   json.loads retornou tipo: {type(data)}")
        except:
            # Se json.loads falhar ou retornar string, usar ast.literal_eval
            print(f"   json.loads falhou, tentando ast.literal_eval...")
            # Se json.loads retornou uma string (dict literal), fazer literal_eval
            if isinstance(data, str):
                data = ast.literal_eval(data)
            else:
                data = json.loads(content)
        
        # Se ainda for string, converter
        if isinstance(data, str):
            print(f"   data ainda é string, fazendo ast.literal_eval...")
            data = ast.literal_eval(data)
        
        print(f"   Tipo final: {type(data)}")
        print(f"   Data: {data}")
        
        # Reescrever como JSON válido com ensure_ascii=False
        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"   ✅ Corrigido!\n")
    
    except Exception as e:
        print(f"   ❌ Erro: {e}\n")
        import traceback
        traceback.print_exc()

print("✅ Correção concluída!")
