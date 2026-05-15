#!/usr/bin/env python3
"""
🚀 SCRIPT SIMPLIFICADO - EXECUTA PIPELINE SEM IMPORTS PESADOS
"""

import sys
from pathlib import Path
from datetime import datetime
import json

# Importar apenas módulos essenciais
try:
    from ml_debug import run_full_debug_report
    from ml_pipeline import train_all_models
except ImportError as e:
    print(f"❌ Erro ao importar módulos: {e}")
    sys.exit(1)


def print_banner(text):
    """Imprime banner visualmente atrativo."""
    width = 100
    print("\n" + "█" * width)
    print("█" + text.center(width - 2) + "█")
    print("█" * width + "\n")


def serialize(obj, depth=0):
    """Serializa objetos numpy para JSON - versão ultra-robusta."""
    import numpy as np
    
    # Limite de profundidade para evitar recursão infinita
    if depth > 50:
        return str(obj)
    
    try:
        if obj is None:
            return None
        
        # Tipos simples que json consegue serializar
        if isinstance(obj, bool):
            return bool(obj)
        if isinstance(obj, int) and not isinstance(obj, np.integer):
            return obj
        if isinstance(obj, float) and not isinstance(obj, np.floating):
            return obj
        if isinstance(obj, str):
            return obj
        
        # Tipos numpy
        if isinstance(obj, np.bool_):
            return bool(obj)
        if isinstance(obj, (np.integer, np.int_, np.int64, np.int32)):
            return int(obj)
        if isinstance(obj, (np.floating, np.float_, np.float64, np.float32)):
            return float(obj)
        
        # Arrays numpy
        if isinstance(obj, np.ndarray):
            return serialize(obj.tolist(), depth=depth+1)
        
        # Dict
        if isinstance(obj, dict):
            return {k: serialize(v, depth=depth+1) for k, v in obj.items()}
        
        # Listas e tuplas
        if isinstance(obj, (list, tuple)):
            return [serialize(item, depth=depth+1) for item in obj]
        
        # Bytes
        if isinstance(obj, bytes):
            return str(obj)
        
        # Fallback para qualquer outro tipo
        return str(obj)
        
    except Exception as e:
        # Se tudo falhar, converter para string
        return str(obj)


def main():
    """Executa pipeline COMPLETO."""
    
    start_time = datetime.now()
    
    print_banner("🚀 PIPELINE SIMPLIFICADO - ML PARA PREVISÃO DE STATUS ACADÊMICO")
    
    # ═════════════════════════════════════════════════════════════════════════════════
    # ETAPA 1: DEBUG DE DADOS
    # ═════════════════════════════════════════════════════════════════════════════════
    
    print_banner("ETAPA 1️⃣  - DEBUG COMPLETO DO SISTEMA DE DADOS")
    
    try:
        debug_results = run_full_debug_report(verbose=True)
        
        # Salvar resultados
        with open("01_debug_results.json", "w", encoding='utf-8') as f:
            json.dump(serialize(debug_results), f, indent=2, ensure_ascii=False)
        
        print("\n✅ Resultados de debug salvos em: 01_debug_results.json")
        
        # Verificação crítica
        leakage_count = debug_results.get("leakage", {}).get("suspicious_count", 0)
        if leakage_count > 0:
            print(f"\n⚠️  ATENÇÃO: {leakage_count} variáveis com potencial data leakage detectadas!")
            print("   As features suspeitas serão AUTOMATICAMENTE REMOVIDAS durante o treinamento.")
    
    except Exception as e:
        print(f"❌ Erro no debug: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # ═════════════════════════════════════════════════════════════════════════════════
    # ETAPA 2: TREINAMENTO DOS MODELOS
    # ═════════════════════════════════════════════════════════════════════════════════
    
    print_banner("ETAPA 2️⃣  - TREINAMENTO DOS MODELOS TEMPORAIS (M1, M2, M3)")
    
    try:
        all_results = train_all_models(verbose=True)
        
        # Salvar resumo
        with open("02_training_summary.json", "w", encoding='utf-8') as f:
            json.dump(serialize(all_results), f, indent=2, ensure_ascii=False)
        
        print("\n✅ Resumo de treinamento salvo em: 02_training_summary.json")
        
        # Verificar treinos bem-sucedidos
        successful = [m for m, r in all_results.items() if r.get("status") == "sucesso"]
        if not successful:
            print("\n❌ Nenhum modelo foi treinado com sucesso!")
            print(f"\nResultados: {all_results}")
            return False
        
        print(f"\n✅ {len(successful)} modelo(s) treinado(s) com sucesso: {', '.join(successful)}")
        
        # Print modelo comparativo
        print("\n" + "█" * 100)
        print("█" + " 📊 RESUMO COMPARATIVO DE MODELOS".center(98) + "█")
        print("█" * 100)
        
        for model_name, model_data in sorted(all_results.items()):
            if model_data["status"] == "sucesso":
                results = model_data["results"]
                print(f"\n{model_name}:")
                print(f"  Acurácia: {results.get('accuracy', 0):.4f}")
                print(f"  F1-Score (weighted): {results.get('f1_weighted', 0):.4f}")
        
        print("\n" + "█" * 100)
        
    except Exception as e:
        print(f"❌ Erro no treinamento: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # ═════════════════════════════════════════════════════════════════════════════════
    # CONCLUIR
    # ═════════════════════════════════════════════════════════════════════════════════
    
    elapsed = datetime.now() - start_time
    
    print_banner("✅ PIPELINE CONCLUÍDO COM SUCESSO!")
    print(f"Tempo total: {elapsed.total_seconds():.1f} segundos")
    print("\n📊 Arquivos gerados:")
    print("  • 01_debug_results.json - Análise detalhada dos dados")
    print("  • 02_training_summary.json - Resultados do treinamento")
    print("  • models/ - Modelos treinados (pkl)")
    
    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Erro não tratado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
