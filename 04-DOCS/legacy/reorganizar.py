#!/usr/bin/env python3
"""Script para reorganizar arquivos conforme estrutura de 8 categorias."""

import os
import shutil
from pathlib import Path

# Mapeamento: arquivo/padrão → pasta destino
REORGANIZACAO = {
    "01-CORE": [
        "cads.py",
        "requirements.txt",
        "escola.db",
    ],
    "02-ML": [
        "gui_ml_advanced.py",
        "gui_ml_integration.py",
        "train_simple.py",
        "config_pesos.json",
        "ml_models",
        "ml_dataset.csv",
    ],
    "03-GUI": [
        "gui_escola.py",
        "gui_predicoes_improved.py",
        "first_init.bat",
    ],
    "04-DOCS": [
        "ARQUITETURA_SISTEMA.md",
        "DOCUMENTACAO_CALCULOS.md",
        "ESTRUTURA_PROJETO.md",
        "IMPLEMENTACAO_ML_AVANCADA.md",
        "INDICE_DOCUMENTACAO.md",
        "QUICKSTART_ML_AVANCADA.md",
        "README_FINAL.md",
        "RESUMO_IMPLEMENTACAO.md",
        "ENTREGA_FINAL.md",
    ],
    "05-TESTS": [
        "test_*.py",
        "debug_*.py",
    ],
    "07-BUILD": [
        "EduNotas.spec",
        "build",
    ],
}

def mover_arquivo(origem, destino):
    """Move arquivo ou pasta de origem para destino."""
    origem_path = Path(origem)
    destino_path = Path(destino)
    
    if not origem_path.exists():
        print(f"❌ Não encontrado: {origem}")
        return False
    
    # Criar diretório destino se não existir
    destino_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        if origem_path.is_dir():
            # Se já existe na destino, remover antes
            if destino_path.exists():
                shutil.rmtree(destino_path)
            shutil.move(str(origem_path), str(destino_path))
        else:
            shutil.move(str(origem_path), str(destino_path))
        
        print(f"✅ Movido: {origem} → {destino}")
        return True
    except Exception as e:
        print(f"❌ Erro ao mover {origem}: {e}")
        return False

def main():
    """Executa reorganização."""
    print("=" * 60)
    print("  REORGANIZANDO ARQUIVOS - ESTRUTURA DE 8 CATEGORIAS")
    print("=" * 60)
    
    root = Path(".")
    total = 0
    sucesso = 0
    
    for pasta_destino, arquivos in REORGANIZACAO.items():
        print(f"\n📁 {pasta_destino}")
        print("-" * 40)
        
        for arquivo in arquivos:
            # Suportar wildcards simples
            if "*" in arquivo:
                # Padrão como debug_*.py
                from glob import glob
                matches = glob(arquivo)
                for match in matches:
                    if Path(match).exists() and not Path(match).is_dir():
                        total += 1
                        if mover_arquivo(match, f"{pasta_destino}/{Path(match).name}"):
                            sucesso += 1
            else:
                # Arquivo ou pasta específica
                if Path(arquivo).exists():
                    total += 1
                    destino = f"{pasta_destino}/{Path(arquivo).name}"
                    if mover_arquivo(arquivo, destino):
                        sucesso += 1
    
    print("\n" + "=" * 60)
    print(f"  RESULTADO: {sucesso}/{total} arquivos movidos com sucesso")
    print("=" * 60)
    print("\n✨ Reorganização completa!")

if __name__ == "__main__":
    main()
