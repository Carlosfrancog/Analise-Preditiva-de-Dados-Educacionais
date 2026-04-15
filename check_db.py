#!/usr/bin/env python3
"""Script para verificar se o BD foi inicializado corretamente."""

import sys
from pathlib import Path

project_root = Path.cwd()
sys.path.insert(0, str(project_root / "01-CORE"))
sys.path.insert(0, str(project_root / "02-ML"))
sys.path.insert(0, str(project_root / "03-GUI"))

try:
    print("Importando cads...")
    import cads
    print("✅ cads importado com sucesso!")
    
    # Testar conexão e tabelas
    print("\nVerificando banco de dados...")
    conn = cads.get_conn()
    c = conn.cursor()
    
    # Listar tabelas
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tabelas = [row[0] for row in c.fetchall()]
    
    print(f"\n📊 Tabelas no banco de dados:")
    for t in sorted(tabelas):
        print(f"   ✅ {t}")
    
    # Verificar ml_features especificamente
    if 'ml_features' in tabelas:
        print("\n✅ Tabela 'ml_features' existe!")
        c.execute("SELECT COUNT(*) FROM ml_features")
        count = c.fetchone()[0]
        print(f"   Registros: {count}")
    else:
        print("\n❌ Tabela 'ml_features' NÃO FOI CRIADA!")
    
    conn.close()
    
    print("\n✅ Banco de dados OK!")
    
except Exception as e:
    print(f"\n❌ Erro: {e}")
    import traceback
    traceback.print_exc()
