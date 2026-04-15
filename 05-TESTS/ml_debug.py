#!/usr/bin/env python3
"""
🔍 DEBUG COMPLETO DO PIPELINE DE DADOS
Detecta data leakage, valida integridade e gera relatório detalhado
"""

import sqlite3
import pandas as pd
import numpy as np
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

DB_PATH = "escola.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ═══════════════════════════════════════════════════════════════════════════════
# 🔍 1. DETECÇÃO DE DATA LEAKAGE
# ═══════════════════════════════════════════════════════════════════════════════

def detect_data_leakage(verbose=True):
    """
    Identifica features que podem estar vazando informação do target.
    
    Critérios:
    - Correlação absoluta > 0.9 com target
    - Features derivadas diretamente do target
    - Variáveis que não estariam disponíveis em tempo de predição
    """
    conn = get_conn()
    df = pd.read_sql_query("""
        SELECT 
            n1_norm, n2_norm, n3_norm, n4_norm,
            media_pond_norm, media_geral_aluno,
            slope_notas, variancia_notas,
            serie_num_norm, pct_materias_ok, media_turma_norm,
            status_encoded
        FROM ml_features
        WHERE status_encoded IS NOT NULL
    """, conn)
    conn.close()
    
    if df.empty:
        return {"erro": "Nenhuma feature gerada. Execute gerar_features_ml() primeiro."}
    
    suspicious = []
    
    # Correlação com target
    correlations = df.corr()['status_encoded'].drop('status_encoded')
    high_corr = correlations[correlations.abs() > 0.9]
    
    if len(high_corr) > 0:
        for feat, corr in high_corr.items():
            suspicious.append({
                "tipo": "ALTA CORRELAÇÃO",
                "feature": feat,
                "correlacao": round(float(corr), 4),
                "risco": "CRÍTICO" if abs(corr) > 0.95 else "ALTO"
            })
    
    # Features ÓBVIAMENTE derivadas do target
    derived_features = {
        "media_pond_norm": {
            "razao": "Calculada diretamente da média ponderada, usada para determinar status",
            "risco": "CRÍTICO"
        },
        "n4_norm": {
            "razao": "N4 é a avaliação final, altamente preditiva do status final",
            "risco": "ALTO"
        }
    }
    
    for feat, info in derived_features.items():
        if feat in df.columns:
            suspicious.append({
                "tipo": "DERIVAÇÃO DIRETA",
                "feature": feat,
                "razao": info["razao"],
                "risco": info["risco"]
            })
    
    result = {
        "total_features": len(df.columns) - 1,
        "suspicious_count": len(suspicious),
        "suspicious": suspicious,
        "correlations_with_target": {
            k: round(float(v), 4) for k, v in correlations.items()
        }
    }
    
    if verbose:
        print("\n" + "="*80)
        print("🚨 DETECÇÃO DE DATA LEAKAGE")
        print("="*80)
        if suspicious:
            print(f"\n⚠️  {len(suspicious)} VARIÁVEIS SUSPEITAS DETECTADAS:\n")
            for i, item in enumerate(suspicious, 1):
                print(f"{i}. [{item['risco']}] {item['feature']}")
                if "correlacao" in item:
                    print(f"   └─ Correlação com target: {item['correlacao']}")
                if "razao" in item:
                    print(f"   └─ Razão: {item['razao']}")
            print("\n" + "─"*80)
            print("RECOMENDAÇÃO: Remover estas features antes do treinamento!")
            print("─"*80)
        else:
            print("✅ Nenhuma variável suspeita detectada.")
        
        print("\nCORRELAÇÕES COM TARGET:")
        for feat, corr in sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True)[:10]:
            print(f"  {feat:25s} : {corr:7.4f}")
    
    return result


# ═══════════════════════════════════════════════════════════════════════════════
# 🔍 2. VALIDAÇÃO DE CONSISTÊNCIA DAS NOTAS
# ═══════════════════════════════════════════════════════════════════════════════

def validate_notes_consistency(verbose=True):
    """
    Verifica:
    - Intervalo válido [0, 10]
    - Valores nulos esperados
    - Duplicatas por aluno×matéria
    - Normalização consistente
    """
    conn = get_conn()
    
    issues = {
        "notas_fora_intervalo": [],
        "normalizacao_inconsistente": [],
        "duplicatas": [],
        "valores_nulos": 0
    }
    
    # Verificar intervalo
    notas_raw = conn.execute("""
        SELECT id, aluno_id, materia_id, n1, n2, n3, n4 FROM notas
    """).fetchall()
    
    for nota in notas_raw:
        for col in ['n1', 'n2', 'n3', 'n4']:
            val = nota[col]
            if val is not None and (val < 0 or val > 10):
                issues["notas_fora_intervalo"].append({
                    "aluno_id": nota['aluno_id'],
                    "materia_id": nota['materia_id'],
                    "campo": col,
                    "valor": val
                })
    
    # Verificar duplicatas
    duplicatas = conn.execute("""
        SELECT aluno_id, materia_id, COUNT(*) as cnt
        FROM notas
        GROUP BY aluno_id, materia_id
        HAVING cnt > 1
    """).fetchall()
    issues["duplicatas"] = [dict(d) for d in duplicatas]
    
    # Verificar nulos
    total_valores = conn.execute("SELECT COUNT(*)*4 FROM notas").fetchone()[0]
    nulos = conn.execute("""
        SELECT COUNT(*) FROM notas
        WHERE n1 IS NULL AND n2 IS NULL AND n3 IS NULL AND n4 IS NULL
    """).fetchone()[0] * 4
    issues["valores_nulos"] = total_valores - nulos
    
    # Validar normalização
    ml_features = conn.execute("""
        SELECT n1, n1_norm, n2, n2_norm, n3, n3_norm
        FROM ml_features
        WHERE n1 IS NOT NULL OR n2 IS NOT NULL OR n3 IS NOT NULL
    """).fetchall()
    
    for row in ml_features:
        for orig_col, norm_col in [('n1', 'n1_norm'), ('n2', 'n2_norm'), ('n3', 'n3_norm')]:
            orig = row[orig_col]
            norm = row[norm_col]
            if orig is not None and norm is not None:
                expected = round(orig / 10.0, 4)
                if abs(norm - expected) > 0.001:
                    issues["normalizacao_inconsistente"].append({
                        "campo": norm_col,
                        "original": orig,
                        "esperado": expected,
                        "obtido": norm
                    })
    
    conn.close()
    
    if verbose:
        print("\n" + "="*80)
        print("✅ VALIDAÇÃO DE INTEGRIDADE DAS NOTAS")
        print("="*80)
        
        if issues["notas_fora_intervalo"]:
            print(f"\n❌ {len(issues['notas_fora_intervalo'])} NOTAS FORA DO INTERVALO [0-10]:")
            for issue in issues["notas_fora_intervalo"][:5]:
                print(f"  Aluno {issue['aluno_id']}, Matéria {issue['materia_id']}: {issue['campo']}={issue['valor']}")
        else:
            print("\n✅ Todas as notas estão dentro do intervalo [0-10]")
        
        if issues["duplicatas"]:
            print(f"\n❌ {len(issues['duplicatas'])} DUPLICATAS POR ALUNO×MATÉRIA:")
            for dup in issues["duplicatas"]:
                print(f"  Aluno {dup['aluno_id']}, Matéria {dup['materia_id']}: {dup['cnt']} registros")
        else:
            print("✅ Nenhuma duplicata detectada")
        
        print(f"\n✅ Total de valores preenchidos: {issues['valores_nulos']}")
        
        if issues["normalizacao_inconsistente"]:
            print(f"\n❌ {len(issues['normalizacao_inconsistente'])} INCONSISTÊNCIAS NA NORMALIZAÇÃO:")
            for inc in issues["normalizacao_inconsistente"][:5]:
                print(f"  {inc['campo']}: esperado {inc['esperado']}, obtido {inc['obtido']}")
        else:
            print("✅ Normalização consistente")
    
    return issues


# ═══════════════════════════════════════════════════════════════════════════════
# 🔍 3. VERIFICAÇÃO DO CÁLCULO DA MÉDIA PONDERADA
# ═══════════════════════════════════════════════════════════════════════════════

def verify_weighted_average(sample_size=10, verbose=True):
    """
    Verifica se a média ponderada está sendo calculada corretamente.
    Pesos: N1=0.20, N2=0.25, N3=0.25, N4=0.30
    """
    conn = get_conn()
    
    rows = conn.execute("""
        SELECT id, n1, n2, n3, n4, media_ponderada, status_label
        FROM ml_features
        WHERE media_ponderada IS NOT NULL
        LIMIT ?
    """, (sample_size,)).fetchall()
    
    conn.close()
    
    issues = []
    pesos = {"n1": 0.20, "n2": 0.25, "n3": 0.25, "n4": 0.30}
    
    for row in rows:
        notas = [row['n1'], row['n2'], row['n3'], row['n4']]
        pesos_list = [0.20, 0.25, 0.25, 0.30]
        
        # Calcular esperado
        soma = sum(p * v for p, v in zip(pesos_list, notas) if v is not None)
        sp = sum(p for p, v in zip(pesos_list, notas) if v is not None)
        esperada = round(soma / sp, 4) if sp > 0 else None
        
        if esperada is not None:
            obtida = round(row['media_ponderada'], 4)
            if abs(obtida - esperada) > 0.01:
                issues.append({
                    "id": row['id'],
                    "notas": notas,
                    "esperada": esperada,
                    "obtida": obtida,
                    "status": row['status_label']
                })
    
    if verbose:
        print("\n" + "="*80)
        print("📊 VERIFICAÇÃO DA MÉDIA PONDERADA")
        print("="*80)
        print(f"Pesos: N1={pesos['n1']}, N2={pesos['n2']}, N3={pesos['n3']}, N4={pesos['n4']}")
        
        if issues:
            print(f"\n❌ {len(issues)} DIVERGÊNCIAS ENCONTRADAS:")
            for issue in issues:
                print(f"  ID {issue['id']}: esperada {issue['esperada']}, obtida {issue['obtida']}")
        else:
            print(f"\n✅ Média ponderada correta em todas as {len(rows)} amostras verificadas")
    
    return issues


# ═══════════════════════════════════════════════════════════════════════════════
# 🔍 4. ANÁLISE DE DISTRIBUIÇÃO DAS CLASSES
# ═══════════════════════════════════════════════════════════════════════════════

def analyze_class_distribution(verbose=True):
    """
    Análise detalhada da distribuição de classes.
    Detecta desbalanceamento e recomenda técnicas de tratamento.
    """
    conn = get_conn()
    
    dist = conn.execute("""
        SELECT status_label, status_encoded, COUNT(*) as count
        FROM ml_features
        WHERE status_encoded IS NOT NULL
        GROUP BY status_encoded
        ORDER BY status_encoded
    """).fetchall()
    
    conn.close()
    
    labels_map = {0: "Reprovado", 1: "Recuperação", 2: "Aprovado"}
    distribution = {}
    total = 0
    
    for row in dist:
        distribution[row['status_label']] = row['count']
        total += row['count']
    
    # Calcular proporções
    proportions = {k: v / total for k, v in distribution.items()}
    
    # Detectar desbalanceamento
    max_prop = max(proportions.values())
    min_prop = min(proportions.values())
    imbalance_ratio = max_prop / min_prop
    
    recommendations = []
    if imbalance_ratio > 3:
        recommendations.append("⚠️  DESBALANCEAMENTO SEVERO (>3x)")
        recommendations.append("  → Use class_weight='balanced' no RandomForest")
        recommendations.append("  → Considere SMOTE ou oversampling da classe minoritária")
    elif imbalance_ratio > 1.5:
        recommendations.append("⚠️  DESBALANCEAMENTO MODERADO (>1.5x)")
        recommendations.append("  → Use class_weight='balanced'")
    else:
        recommendations.append("✅ Distribuição equilibrada")
    
    if verbose:
        print("\n" + "="*80)
        print("📈 DISTRIBUIÇÃO DAS CLASSES")
        print("="*80)
        print(f"\nTotal de amostras: {total}\n")
        
        for status, count in distribution.items():
            prop = proportions[status] * 100
            bar_len = int(prop / 2)
            bar = "█" * bar_len + "░" * (50 - bar_len)
            print(f"{status:15s}: {count:4d} ({prop:5.1f}%) {bar}")
        
        print(f"\nRazão de desbalanceamento: {imbalance_ratio:.2f}x")
        print("\nRecomendações:")
        for rec in recommendations:
            print(f"  {rec}")
    
    return {
        "distribuicao": distribution,
        "proporcoes": proportions,
        "total": total,
        "imbalance_ratio": imbalance_ratio,
        "recomendacoes": recommendations
    }


# ═══════════════════════════════════════════════════════════════════════════════
# 🔍 5. VALIDAÇÃO DA FEATURE SLOPE_NOTAS
# ═══════════════════════════════════════════════════════════════════════════════

def validate_slope_feature(verbose=True):
    """
    Verifica se slope_notas está normalizado corretamente (-1 a +1).
    Correlação com melhoria de desempenho.
    """
    conn = get_conn()
    
    df = pd.read_sql_query("""
        SELECT n1, n2, n3, n4, slope_notas, status_encoded
        FROM ml_features
        WHERE slope_notas IS NOT NULL
    """, conn)
    conn.close()
    
    # Validar intervalo
    out_of_range = df[(df['slope_notas'] < -1) | (df['slope_notas'] > 1)]
    
    # Correlação com melhoria
    if not df.empty and 'status_encoded' in df.columns:
        correlation = df['slope_notas'].corr(df['status_encoded'])
    else:
        correlation = np.nan
    
    # Casos extremos
    positive_slope = len(df[df['slope_notas'] > 0.5])
    negative_slope = len(df[df['slope_notas'] < -0.5])
    stable = len(df[abs(df['slope_notas']) <= 0.2])
    
    if verbose:
        print("\n" + "="*80)
        print("📊 VALIDAÇÃO DE SLOPE_NOTAS (Tendência de Crescimento)")
        print("="*80)
        
        if len(out_of_range) > 0:
            print(f"\n❌ {len(out_of_range)} VALORES FORA DO INTERVALO [-1, +1]")
        else:
            print(f"\n✅ Todos os {len(df)} valores estão no intervalo [-1, +1]")
        
        print(f"\nComposição do dataset:")
        print(f"  Crescimento positivo (slope > 0.5 ): {positive_slope:4d} ({100*positive_slope/len(df):.1f}%)")
        print(f"  Decrescimento (slope < -0.5       ): {negative_slope:4d} ({100*negative_slope/len(df):.1f}%)")
        print(f"  Estável (|slope| <= 0.2           ): {stable:4d} ({100*stable/len(df):.1f}%)")
        
        print(f"\nCorrelação com status: {correlation:.4f}")
        if abs(correlation) > 0.3:
            print("  ✅ Correlação significativa com performance")
        else:
            print("  ⚠️  Correlação fraca - feature pode ter baixo impacto")
    
    return {
        "total": len(df),
        "fora_intervalo": len(out_of_range),
        "positive_trend": positive_slope,
        "negative_trend": negative_slope,
        "stable": stable,
        "correlacao_com_status": float(correlation) if not np.isnan(correlation) else None
    }


# ═══════════════════════════════════════════════════════════════════════════════
# 🔍 6. VERIFICAÇÃO DE VARIÂNCIA
# ═══════════════════════════════════════════════════════════════════════════════

def validate_variance_feature(verbose=True):
    """
    Verifica se variancia_notas está normalizada (0-1) e correlacionada com
    comportamento inconsistente.
    """
    conn = get_conn()
    
    df = pd.read_sql_query("""
        SELECT n1, n2, n3, n4, variancia_notas, status_encoded
        FROM ml_features
        WHERE variancia_notas IS NOT NULL AND status_encoded IS NOT NULL
    """, conn)
    conn.close()
    
    # Validar intervalo
    out_of_range = df[(df['variancia_notas'] < 0) | (df['variancia_notas'] > 1)]
    
    # Correlação com status
    if not df.empty:
        correlation = df['variancia_notas'].corr(df['status_encoded'])
        # Alta variância deveria correlacionar com status ruim (reprovados)
    else:
        correlation = np.nan
    
    # Distribuição
    low_var = len(df[df['variancia_notas'] < 0.2])
    mid_var = len(df[(df['variancia_notas'] >= 0.2) & (df['variancia_notas'] < 0.6)])
    high_var = len(df[df['variancia_notas'] >= 0.6])
    
    if verbose:
        print("\n" + "="*80)
        print("📊 VALIDAÇÃO DE VARIANCIA_NOTAS (Consistência do Desempenho)")
        print("="*80)
        
        if len(out_of_range) > 0:
            print(f"\n❌ {len(out_of_range)} VALORES FORA DO INTERVALO [0, 1]")
        else:
            print(f"\n✅ Todos os {len(df)} valores estão no intervalo [0, 1]")
        
        print(f"\nDistribuição de variância:")
        print(f"  Baixa (< 0.2    ): {low_var:4d} ({100*low_var/len(df):.1f}%) - Consistente")
        print(f"  Média (0.2-0.6  ): {mid_var:4d} ({100*mid_var/len(df):.1f}%) - Moderado")
        print(f"  Alta (>= 0.6    ): {high_var:4d} ({100*high_var/len(df):.1f}%) - Inconsistente")
        
        print(f"\nCorrelação com status: {correlation:.4f}")
        if correlation < -0.2:
            print("  ✅ Alta variância correlaciona com pior performance (esperado)")
        else:
            print("  ⚠️  Correlação não observada - feature pode ter baixo valor")
    
    return {
        "total": len(df),
        "fora_intervalo": len(out_of_range),
        "baixa": low_var,
        "media": mid_var,
        "alta": high_var,
        "correlacao_com_status": float(correlation) if not np.isnan(correlation) else None
    }


# ═══════════════════════════════════════════════════════════════════════════════
# 🔍 7. CHECAGEM DE INTEGRIDADE DO CONTEXTO
# ═══════════════════════════════════════════════════════════════════════════════

def validate_context_features(verbose=True):
    """
    Valida:
    - media_turma_norm: calculada sem incluir próprio aluno?
    - pct_materias_ok: considera dados históricos válidos?
    """
    conn = get_conn()
    
    # Amostra de features
    sample = pd.read_sql_query("""
        SELECT 
            aluno_id, materia_id, aluno_nome, sala_nome,
            media_turma_norm, pct_materias_ok, status_encoded
        FROM ml_features
        WHERE media_turma_norm IS NOT NULL
        LIMIT 20
    """, conn)
    
    # Verificar limites
    turma_norm_valid = sample[(sample['media_turma_norm'] >= 0) & (sample['media_turma_norm'] <= 1)]
    pct_valid = sample[(sample['pct_materias_ok'] >= 0) & (sample['pct_materias_ok'] <= 1)]
    
    conn.close()
    
    issues = []
    if len(turma_norm_valid) != len(sample):
        issues.append("media_turma_norm fora do intervalo [0,1]")
    if len(pct_valid) != len(sample):
        issues.append("pct_materias_ok fora do intervalo [0,1]")
    
    if verbose:
        print("\n" + "="*80)
        print("🔗 VALIDAÇÃO DE FEATURES DE CONTEXTO")
        print("="*80)
        
        print(f"\nTotal de amostras verificadas: {len(sample)}")
        print(f"  media_turma_norm em [0,1]   : {len(turma_norm_valid)}/{len(sample)} ✅" if len(turma_norm_valid) == len(sample) else f"  media_turma_norm em [0,1]   : {len(turma_norm_valid)}/{len(sample)} ❌")
        print(f"  pct_materias_ok em [0,1]    : {len(pct_valid)}/{len(sample)} ✅" if len(pct_valid) == len(sample) else f"  pct_materias_ok em [0,1]    : {len(pct_valid)}/{len(sample)} ❌")
        
        if issues:
            print(f"\n⚠️  Problemas encontrados:")
            for issue in issues:
                print(f"  - {issue}")
    
    return {
        "amostras_verificadas": len(sample),
        "turma_norm_validas": len(turma_norm_valid),
        "pct_materias_ok_validas": len(pct_valid),
        "issues": issues
    }


# ═══════════════════════════════════════════════════════════════════════════════
# 🔍 8. DETECÇÃO DE OUTLIERS
# ═══════════════════════════════════════════════════════════════════════════════

def detect_outliers(verbose=True):
    """
    Detecta padrões impossíveis ou anomalias nos dados.
    """
    conn = get_conn()
    
    df = pd.read_sql_query("""
        SELECT 
            aluno_id, materia_id, aluno_nome, materia_nome,
            n1, n2, n3, n4,
            slope_notas, variancia_notas, media_ponderada, status_encoded
        FROM ml_features
        WHERE status_encoded IS NOT NULL
    """, conn)
    conn.close()
    
    outliers = {
        "notas_negativas": [],
        "notas_acima_10": [],
        "inconsistencias_ordercm": [],
        "valor_normalizacao": []
    }
    
    # Verificar notas inválidas
    for col in ['n1', 'n2', 'n3', 'n4']:
        invalidas = df[df[col] < 0]
        if len(invalidas) > 0:
            outliers["notas_negativas"].extend(invalidas.index.tolist())
        
        invalidas = df[df[col] > 10]
        if len(invalidas) > 0:
            outliers["notas_acima_10"].extend(invalidas.index.tolist())
    
    # Outliers por IQR em features numéricas
    for feat in ['slope_notas', 'variancia_notas', 'media_ponderada']:
        Q1 = df[feat].quantile(0.25)
        Q3 = df[feat].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        outlier_mask = (df[feat] < lower) | (df[feat] > upper)
        if outlier_mask.sum() > 0:
            outliers[f"outlier_{feat}"] = outlier_mask.sum()
    
    if verbose:
        print("\n" + "="*80)
        print("⚠️  DETECÇÃO DE OUTLIERS E ANOMALIAS")
        print("="*80)
        
        total_issues = sum(len(v) if isinstance(v, list) else v for v in outliers.values())
        print(f"\nTotal de anomalias: {total_issues}\n")
        
        if outliers["notas_negativas"]:
            print(f"❌ Notas negativas encontradas: {len(outliers['notas_negativas'])}")
        else:
            print(f"✅ Nenhuma nota negativa")
        
        if outliers["notas_acima_10"]:
            print(f"❌ Notas acima de 10 encontradas: {len(outliers['notas_acima_10'])}")
        else:
            print(f"✅ Nenhuma nota acima de 10")
        
        for key, value in outliers.items():
            if isinstance(value, int) and value > 0:
                print(f"⚠️  Outliers em {key}: {value}")
    
    return outliers


# ═══════════════════════════════════════════════════════════════════════════════
# 🔍 9. ANÁLISE DE DRIFT DE DADOS
# ═══════════════════════════════════════════════════════════════════════════════

def analyze_data_drift(verbose=True):
    """
    Detecta mudanças na distribuição de features ao longo de turmas/anos.
    """
    conn = get_conn()
    
    df = pd.read_sql_query("""
        SELECT 
            sala_nome, serie_num, status_encoded,
            n1_norm, n2_norm, n3_norm,
            slope_notas, variancia_notas,
            media_geral_aluno, pct_materias_ok
        FROM ml_features
        WHERE status_encoded IS NOT NULL
    """, conn)
    conn.close()
    
    if df.empty:
        return {"erro": "Sem dados suficientes"}
    
    # Análise por turma
    drift_by_class = {}
    for sala in df['sala_nome'].unique():
        sala_df = df[df['sala_nome'] == sala]
        
        # Distribuição de status nesta turma
        dist = sala_df['status_encoded'].value_counts().to_dict()
        
        # Média de features
        mean_features = sala_df[['n1_norm', 'n2_norm', 'n3_norm', 'slope_notas', 
                                  'media_geral_aluno', 'pct_materias_ok']].mean()
        
        drift_by_class[sala] = {
            "n_alunos": len(sala_df),
            "distribuicao": dist,
            "media_n1_norm": float(mean_features['n1_norm']),
            "media_slope": float(mean_features['slope_notas']),
            "media_pct_ok": float(mean_features['pct_materias_ok'])
        }
    
    if verbose:
        print("\n" + "="*80)
        print("📊 ANÁLISE DE DRIFT DE DADOS")
        print("="*80)
        
        print(f"\nCobertura: {len(drift_by_class)} turmas únicas\n")
        
        for sala, stats in sorted(drift_by_class.items()):
            print(f"{sala} ({stats['n_alunos']} alunos):")
            print(f"  Status: {stats['distribuicao']}")
            print(f"  Média N1_norm: {stats['media_n1_norm']:.3f}")
            print(f"  Média Slope:   {stats['media_slope']:.3f}")
            print(f"  Média %OK:     {stats['media_pct_ok']:.3f}")
            print()
    
    return drift_by_class


# ═══════════════════════════████, RELATÓRIO EXECUTIVO
# ═══════════════════════════════════════════════════════════════════════════════

def run_full_debug_report(verbose=True):
    """
    Executa TODOS os testes de debug e gera relatório consolidado.
    """
    print("\n" + "█"*80)
    print("█" + " "*78 + "█")
    print("█" + "🔍 SISTEMA COMPLETO DE DEBUG - PIPELINE DE DADOS ML".center(78) + "█")
    print("█" + " "*78 + "█")
    print("█"*80)
    
    results = {}
    
    # Executar todos os testes
    results["leakage"] = detect_data_leakage(verbose)
    results["consistency"] = validate_notes_consistency(verbose)
    results["weighted_avg"] = verify_weighted_average(verbose=verbose)
    results["class_dist"] = analyze_class_distribution(verbose)
    results["slope"] = validate_slope_feature(verbose)
    results["variance"] = validate_variance_feature(verbose)
    results["context"] = validate_context_features(verbose)
    results["outliers"] = detect_outliers(verbose)
    results["drift"] = analyze_data_drift(verbose)
    
    # Relatório final
    print("\n" + "█"*80)
    print("█" + " "*78 + "█")
    print("█" + "📋 RESUMO EXECUTIVO".center(78) + "█")
    print("█" + " "*78 + "█")
    print("█"*80)
    
    print("\n✅ STATUS DE QUALIDADE DOS DADOS:\n")
    
    # Data Leakage
    suspicious_count = results["leakage"].get("suspicious_count", 0)
    if suspicious_count == 0:
        print("  [✅] Data Leakage: Nenhuma variável suspeita")
    else:
        print(f"  [❌] Data Leakage: {suspicious_count} variáveis suspeitas - REMOVER DO MODELO")
    
    # Integridade
    issues = results["consistency"]
    if issues["notas_fora_intervalo"]:
        print(f"  [❌] Notas inválidas: {len(issues['notas_fora_intervalo'])}")
    else:
        print("  [✅] Integridade: Todas as notas válidas")
    
    # Média ponderada
    if results["weighted_avg"]:
        print(f"  [❌] Média ponderada: {len(results['weighted_avg'])} divergências")
    else:
        print("  [✅] Média ponderada: Cálculos corretos")
    
    # Distribuição de classes
    imbalance = results["class_dist"]["imbalance_ratio"]
    if imbalance > 3:
        print(f"  [⚠️ ] Distribuição: Desbalanceamento severo ({imbalance:.1f}x)")
    elif imbalance > 1.5:
        print(f"  [⚠️ ] Distribuição: Desbalanceamento moderado ({imbalance:.1f}x)")
    else:
        print(f"  [✅] Distribuição: Equivalrada ({imbalance:.1f}x)")
    
    # Outliers
    outlier_count = sum(len(v) if isinstance(v, list) else v 
                       for v in results["outliers"].values())
    if outlier_count == 0:
        print("  [✅] Outliers: Nenhum detectado")
    else:
        print(f"  [⚠️ ] Outliers: {outlier_count} anomalias")
    
    print("\n" + "─"*80)
    print("🎯 PRÓXIMOS PASSOS:")
    print("─"*80)
    print("""
1. Se data leakage detectado → REMOVER features suspeitas
2. Se desbalanceamento > 1.5x → use class_weight='balanced' no modelo
3. Treinar modelos temporais: M1 (n1), M2 (n1+n2), M3 (n1+n2+n3)
4. Executar feature importance e SHAP analysis
5. Validar cross-validation com estratificação por status
    """)
    print("█"*80 + "\n")
    
    return results


if __name__ == "__main__":
    # Executar debug completo
    results = run_full_debug_report(verbose=True)
    
    # Exportar resultados para arquivo JSON
    import json
    
    # Serializar resultados
    def serialize(obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, list):
            return [serialize(i) for i in obj]
        elif isinstance(obj, dict):
            return {k: serialize(v) for k, v in obj.items()}
        return obj
    
    with open("debug_results.json", "w", encoding="utf-8") as f:
        json.dump(serialize(results), f, indent=2, ensure_ascii=False)
    
    print("✅ Resultados salvos em debug_results.json")
