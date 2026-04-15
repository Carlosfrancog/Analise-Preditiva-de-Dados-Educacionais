#!/usr/bin/env python3
"""
Script de inicialização - Executa a aplicação do sistema escolar
Execute este arquivo a partir da pasta raiz do projeto
"""

import sys
import os
from pathlib import Path

# Definir diretório de trabalho como a pasta raiz do projeto
project_root = Path(__file__).parent
os.chdir(str(project_root))

# Adicionar pastas ao path
sys.path.insert(0, str(project_root / "01-CORE"))
sys.path.insert(0, str(project_root / "02-ML"))
sys.path.insert(0, str(project_root / "03-GUI"))

# Agora importar e executar
from gui_escola import main as gui_main

if __name__ == "__main__":
    gui_main()
