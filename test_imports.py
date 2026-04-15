#!/usr/bin/env python3
"""Script para testar se tudo funciona sem abrir GUI."""

import sys
from pathlib import Path

project_root = Path.cwd()
sys.path.insert(0, str(project_root / "01-CORE"))
sys.path.insert(0, str(project_root / "02-ML"))
sys.path.insert(0, str(project_root / "03-GUI"))

print("=" * 60)
print("TESTE DE IMPORTS E BD")
print("=" * 60)

try:
    # 1. Testar cads
    print("\n1️⃣ Testando cads...")
    import cads
    print(f"   ✅ cads importado")
    print(f"   DB_PATH: {cads.DB_PATH}")
    print(f"   Existe: {Path(cads.DB_PATH).exists()}")
    
    # 2. Testar GUI ML integration
    print("\n2️⃣ Testando gui_ml_integration...")
    from gui_ml_integration import DisciplinePerformanceAnalyzer, MLModelLoader
    print(f"   ✅ DisciplinePerformanceAnalyzer importado")
    print(f"   ✅ MLModelLoader importado")
    
    # 3. Teste de conexão
    print("\n3️⃣ Testando conexão com BD...")
    conn = cads.get_conn()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM alunos")
    count = c.fetchone()[0]
    conn.close()
    print(f"   ✅ Tabela 'alunos' OK ({count} registros)")
    
    # 4. Teste de ml_features
    print("\n4️⃣ Testando tabela ml_features...")
    conn = cads.get_conn()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM ml_features")
    count = c.fetchone()[0]
    conn.close()
    print(f"   ✅ Tabela 'ml_features' OK ({count} registros)")
    
    print("\n" + "=" * 60)
    print("✅ TODOS OS TESTES PASSARAM!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
