#!/usr/bin/env python3
"""
📖 EXEMPLOS PRÁTICOS DE USO DO SISTEMA DE ML
Demonstra como usar cada componente
"""

# =============================================================================
# EXEMPLO 1: Debug Completo de Dados
# =============================================================================

def exemplo_1_debug_dados():
    """
    Executar todas as validações de dados.
    Use isso ANTES de treinar para garantir qualidade.
    """
    print("\n" + "="*80)
    print("EXEMPLO 1: Debug Completo de Dados")
    print("="*80 + "\n")
    
    from ml_debug import (
        detect_data_leakage,
        validate_notes_consistency,
        verify_weighted_average,
        analyze_class_distribution,
        detect_outliers,
        run_full_debug_report
    )
    
    # Opção 1: Executar tudo de uma vez
    results = run_full_debug_report(verbose=True)
    
    # Opção 2: Validações individuais
    # leakage = detect_data_leakage(verbose=True)
    # consistency = validate_notes_consistency(verbose=True)
    # avg = verify_weighted_average(verbose=True)
    # dist = analyze_class_distribution(verbose=True)
    # outliers = detect_outliers(verbose=True)
    
    return results


# =============================================================================
# EXEMPLO 2: Treinar um Único Modelo
# =============================================================================

def exemplo_2_treinar_um_modelo():
    """
    Treina apenas o modelo M3 (mais completo).
    """
    print("\n" + "="*80)
    print("EXEMPLO 2: Treinar Modelo M3")
    print("="*80 + "\n")
    
    from ml_pipeline import train_random_forest, save_model
    
    # Treinar modelo
    model, results, mapping = train_random_forest(
        model_type="M3",
        test_size=0.2,
        random_state=42,
        verbose=True
    )
    
    # Salvar modelo
    model_path = save_model(model, results, mapping, model_name="meu_modelo_m3")
    print(f"\n✅ Modelo salvo em: {model_path}")
    
    return model, results, mapping


# =============================================================================
# EXEMPLO 3: Treinar Todos os Modelos
# =============================================================================

def exemplo_3_treinar_todos():
    """
    Treina M1, M2 e M3 sequencialmente.
    Cada modelo usa um subset diferente de features.
    """
    print("\n" + "="*80)
    print("EXEMPLO 3: Treinar Todos os Modelos (M1, M2, M3)")
    print("="*80 + "\n")
    
    from ml_pipeline import train_all_models
    
    all_results = train_all_models(verbose=True)
    
    # Análise rápida
    print("\n" + "─"*80)
    print("RESUMO:")
    for model_type, result in all_results.items():
        if result["status"] == "sucesso":
            acc = result["results"]["accuracy"]
            f1 = result["results"]["f1_macro"]
            print(f"  {model_type}: Accuracy={acc:.4f}, F1={f1:.4f}")
    
    return all_results


# =============================================================================
# EXEMPLO 4: Carregar e Usar um Modelo Treinado
# =============================================================================

def exemplo_4_usar_modelo():
    """
    Carrega um modelo já treinado e faz predições.
    """
    print("\n" + "="*80)
    print("EXEMPLO 4: Usar Modelo em Produção")
    print("="*80 + "\n")
    
    from pathlib import Path
    from ml_pipeline import load_model, predict_student_status, MODELS_DIR
    
    # Encontrar modelo M3 mais recente
    model_dirs = list(MODELS_DIR.glob("RF_M3_*"))
    if not model_dirs:
        print("❌ Nenhum modelo M3 encontrado!")
        return
    
    model_dir = max(model_dirs, key=lambda p: p.stat().st_mtime)
    print(f"Usando modelo: {model_dir.name}\n")
    
    # Carregar
    model, results, mapping = load_model(model_dir)
    print(f"✅ Modelo carregado")
    print(f"   Features: {mapping['feature_names']}")
    print(f"   Classes: {mapping['class_labels']}")
    print(f"   Accuracy no teste: {results['accuracy']:.4f}")
    
    # Predição para um aluno específico
    print(f"\n{'─'*80}")
    print("Fazendo predição para aluno_id=1, materia_id=1:\n")
    
    prediction, error = predict_student_status(model_dir, aluno_id=1, materia_id=1)
    
    if error is None:
        print(f"Nome do aluno: {prediction['aluno_nome']}")
        print(f"Matéria: {prediction['materia_nome']}")
        print(f"Classe predita: {prediction['predicted_label']}")
        print(f"Confiança: {prediction['confidence']:.2%}\n")
        print("Probabilidades:")
        for label, prob in sorted(prediction['probabilities'].items(), 
                                 key=lambda x: x[1], reverse=True):
            bar = "█" * int(prob * 40)
            print(f"  {label:15s}: {prob:.2%} {bar}")
    else:
        print(f"❌ Erro: {error}")
    
    return model, results, mapping


# =============================================================================
# EXEMPLO 5: Análise de Feature Importance
# =============================================================================

def exemplo_5_feature_importance():
    """
    Analisa qual features são mais importantes para as predições.
    """
    print("\n" + "="*80)
    print("EXEMPLO 5: Análise de Feature Importance")
    print("="*80 + "\n")
    
    from pathlib import Path
    from ml_pipeline import MODELS_DIR
    from ml_models import analyze_feature_importance
    
    # Encontrar modelo M3
    model_dirs = list(MODELS_DIR.glob("RF_M3_*"))
    if not model_dirs:
        print("❌ Nenhum modelo M3 encontrado!")
        return
    
    model_dir = max(model_dirs, key=lambda p: p.stat().st_mtime)
    
    # Análise
    analysis = analyze_feature_importance(
        model_dir=model_dir,
        top_n=10,
        plot=True,
        save_path="feature_importance.png"
    )
    
    print(f"\n✅ Gráfico salvo em: feature_importance.png")
    
    return analysis


# =============================================================================
# EXEMPLO 6: Análise de Correlação Feature-Target
# =============================================================================

def exemplo_6_correlacao():
    """
    Mostra correlação (linear) entre cada feature e o target.
    """
    print("\n" + "="*80)
    print("EXEMPLO 6: Correlação Feature-Target")
    print("="*80 + "\n")
    
    from pathlib import Path
    from ml_pipeline import MODELS_DIR
    from ml_models import analyze_feature_target_correlation
    
    model_dirs = list(MODELS_DIR.glob("RF_M3_*"))
    if not model_dirs:
        print("❌ Nenhum modelo M3 encontrado!")
        return
    
    model_dir = max(model_dirs, key=lambda p: p.stat().st_mtime)
    
    correlations = analyze_feature_target_correlation(
        model_dir=model_dir,
        plot=True
    )
    
    print(f"\n✅ Correlações calculadas")
    
    return correlations


# =============================================================================
# EXEMPLO 7: Comparar Todos os Modelos
# =============================================================================

def exemplo_7_comparar_modelos():
    """
    Compara M1, M2 e M3 lado a lado.
    Ajuda a escolher qual usar em produção.
    """
    print("\n" + "="*80)
    print("EXEMPLO 7: Comparar Modelos M1, M2, M3")
    print("="*80 + "\n")
    
    from ml_models import compare_models
    
    compare_models()
    
    print(f"\n✅ Análise completa exibida acima")


# =============================================================================
# EXEMPLO 8: Análise SHAP (explicabilidade avançada)
# =============================================================================

def exemplo_8_shap_analysis():
    """
    Análise SHAP para entender PORQUE o modelo faz cada predição.
    Requer: pip install shap
    """
    print("\n" + "="*80)
    print("EXEMPLO 8: Análise SHAP (Explicabilidade)")
    print("="*80 + "\n")
    
    try:
        from pathlib import Path
        from ml_pipeline import MODELS_DIR
        from ml_models import analyze_with_shap
        
        model_dirs = list(MODELS_DIR.glob("RF_M3_*"))
        if not model_dirs:
            print("❌ Nenhum modelo M3 encontrado!")
            return
        
        model_dir = max(model_dirs, key=lambda p: p.stat().st_mtime)
        
        shap_values, explainer = analyze_with_shap(
            model_dir=model_dir,
            sample_size=50,
            plot=True
        )
        
        print(f"\n✅ Análise SHAP completa")
        
    except ImportError:
        print("⚠️  SHAP não instalado")
        print("   Instale com: pip install shap")


# =============================================================================
# EXEMPLO 9: Geração de Relatório Completo
# =============================================================================

def exemplo_9_relatorio_completo():
    """
    Gera relatório visual completo com todos os gráficos.
    """
    print("\n" + "="*80)
    print("EXEMPLO 9: Gerar Relatório Completo")
    print("="*80 + "\n")
    
    from pathlib import Path
    from ml_pipeline import MODELS_DIR
    from ml_models import generate_explainability_report
    
    for model_type in ["M1", "M2", "M3"]:
        model_dirs = list(MODELS_DIR.glob(f"RF_{model_type}_*"))
        if model_dirs:
            model_dir = max(model_dirs, key=lambda p: p.stat().st_mtime)
            print(f"\nGerando relatório para {model_type}...\n")
            generate_explainability_report(model_dir, model_type=model_type)


# =============================================================================
# EXEMPLO 10: Pipeline Completo (do Zero)
# =============================================================================

def exemplo_10_pipeline_completo():
    """
    Executa o pipeline COMPLETO.
    Equivalente a rodar: python run_ml_pipeline.py
    """
    print("\n" + "="*80)
    print("EXEMPLO 10: Pipeline Completo")
    print("="*80 + "\n")
    
    from run_ml_pipeline import run_complete_pipeline
    
    success = run_complete_pipeline()
    
    if success:
        print("\n✅ Pipeline executado com sucesso!")
    else:
        print("\n❌ Pipeline falhou!")


# =============================================================================
# MENU INTERATIVO
# =============================================================================

def main():
    """Menu para escolher qual exemplo executar."""
    
    print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║                                                                                ║
║         📖 EXEMPLOS PRÁTICOS - SISTEMA DE ML PARA STATUS ACADÊMICO             ║
║                                                                                ║
╚════════════════════════════════════════════════════════════════════════════════╝

Escolha um exemplo para executar:

1️⃣  Debug Completo de Dados
   └─ Valida integridade, detecta leakage, analisa distribuição

2️⃣  Treinar Modelo M3 (mais completo)
   └─ Treina usando N1, N2, N3 + comportamento + contexto

3️⃣  Treinar Todos os Modelos (M1, M2, M3)
   └─ Modelos temporais com diferentes níveis de informação

4️⃣  Usar Modelo em Produção
   └─ Carrega modelo salvo e faz predições para alunos

5️⃣  Análise de Feature Importance
   └─ Mostra quais features são mais importantes

6️⃣  Correlação Feature-Target
   └─ Análise linear de relação entre features e target

7️⃣  Comparar Modelos (M1 vs M2 vs M3)
   └─ Tabela comparativa e recomendação

8️⃣  Análise SHAP (Explicabilidade Avançada)
   └─ Entender PORQUE cada predição é feita (requer: pip install shap)

9️⃣  Gerar Relatório Completo
   └─ Cria gráficos e análises para todos os modelos

🔟  Pipeline Completo (do Zero)
   └─ Executa tudo: debug → treinamento → análise → comparação

0️⃣  Sair

    """)
    
    escolha = input("Digite o número do exemplo (0-10): ").strip()
    
    exemplos = {
        "1": ("Debug Completo", exemplo_1_debug_dados),
        "2": ("Treinar M3", exemplo_2_treinar_um_modelo),
        "3": ("Treinar Todos", exemplo_3_treinar_todos),
        "4": ("Usar Modelo", exemplo_4_usar_modelo),
        "5": ("Feature Importance", exemplo_5_feature_importance),
        "6": ("Correlação", exemplo_6_correlacao),
        "7": ("Comparar Modelos", exemplo_7_comparar_modelos),
        "8": ("SHAP Analysis", exemplo_8_shap_analysis),
        "9": ("Relatório Completo", exemplo_9_relatorio_completo),
        "10": ("Pipeline Completo", exemplo_10_pipeline_completo),
    }
    
    if escolha == "0":
        print("\n👋 Até logo!")
        return
    
    if escolha in exemplos:
        nome, func = exemplos[escolha]
        print(f"\n▶️  Executando: {nome}\n")
        try:
            func()
            print(f"\n✅ {nome} concluído!")
        except Exception as e:
            print(f"\n❌ Erro: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("\n❌ Opção inválida!")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Execução direta por linha de comando
        exemplo_num = sys.argv[1]
        
        exemplos = {
            "1": exemplo_1_debug_dados,
            "2": exemplo_2_treinar_um_modelo,
            "3": exemplo_3_treinar_todos,
            "4": exemplo_4_usar_modelo,
            "5": exemplo_5_feature_importance,
            "6": exemplo_6_correlacao,
            "7": exemplo_7_comparar_modelos,
            "8": exemplo_8_shap_analysis,
            "9": exemplo_9_relatorio_completo,
            "10": exemplo_10_pipeline_completo,
        }
        
        if exemplo_num in exemplos:
            exemplos[exemplo_num]()
        else:
            print(f"❌ Exemplo '{exemplo_num}' não encontrado!")
    
    else:
        # Menu interativo
        main()
