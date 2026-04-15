#!/usr/bin/env python3
"""Debug do caso: N1=1.0, N2=9.0 em Química"""
import cads
from gui_ml_integration import load_ml_models

ml = load_ml_models()

print(f"\n{'='*80}")
print(f"🔍 DEBUG: Aluno com N1=1.0, N2=9.0 (Melhora de 800%!)")
print(f"{'='*80}\n")

# Simulação dos dados
n1_raw = 1.0
n2_raw = 9.0
n3_raw = None
n4_raw = None

print(f"DADOS DE ENTRADA:")
print(f"  N1: {n1_raw}")
print(f"  N2: {n2_raw}")
print(f"  N3: {n3_raw}")
print(f"  N4: {n4_raw}\n")

# Normaliza
n1 = n1_raw / 10
n2 = n2_raw / 10

# Calcula features
slope = (n2 - n1) if (n1_raw and n2_raw) else 0
variancia = abs(n1 - n2)
media_n12 = (n1_raw + n2_raw) / 2
media_norm = media_n12 / 10

print(f"CÁLCULOS:")
print(f"  Slope: ({n2:.1f} - {n1:.1f}) = {slope:.2f}")
print(f"  Slope % : ({n2_raw} - {n1_raw}) / {n1_raw} = {(n2_raw - n1_raw) / n1_raw * 100:.0f}%")
print(f"  Variância: |{n1:.2f} - {n2:.2f}| = {variancia:.2f}")
print(f"  Média N1+N2: {media_n12:.1f}")
print(f"  Status Atual: ", end="")

if media_n12 < 5:
    status_atual = 0
    print("❌ REPROVADO")
elif media_n12 < 6:
    status_atual = 1
    print("⚠️ RECUPERAÇÃO")
else:
    status_atual = 2
    print("✅ APROVADO")

print()

# Features para modelo
features = [n1, n2, 0, 0, slope, variancia, media_norm, 0.5, 0.5]

print(f"FEATURES PARA MODELO:")
print(f"  [{n1:.2f}, {n2:.2f}, 0, 0, {slope:.2f}, {variancia:.2f}, {media_norm:.2f}, 0.5, 0.5]")
print()

# Predição
pred, proba = ml.predict("RF_M3", features)
predicted_status = int(pred) if pred is not None else -1

print(f"PREDIÇÃO DO MODELO:")
print(f"  Status Predito: {predicted_status} ", end="")

status_map = {0: "❌ Reprovado", 1: "⚠️ Recuperação", 2: "✅ Aprovado"}
print(status_map.get(predicted_status, "?"))
print(f"  Probabilidades: {proba}")
print()

# Análise
print(f"COMPARAÇÃO:")
print(f"  Predito ({predicted_status}) vs Atual ({status_atual})")

if predicted_status > status_atual:
    print(f"  → Modelo prevê MELHORA ✨")
    print(f"     Interpretação: Vai melhorar (predicted melhor que atual)")
elif predicted_status < status_atual:
    print(f"  → Modelo prevê PIORA ⚠️")
    print(f"     Interpretação: Vai piorar (predicted pior que atual)")
else:
    print(f"  → Modelo prevê MESMA COISA →")
    print(f"     Interpretação: Vai manter (predicted igual ao atual)")

print()
print(f"{'='*80}")
print(f"O PROBLEMA:")
print(f"{'='*80}")
print()
print(f"❌ Interpretação Atual (ERRADA):")
print(f"   'Variância alta (8pts) + slope negativo = instabilidade ruim'")
print(f"   Mas slope = {slope:.2f} não é negativo!")
print()
print(f"✅ Interpretação Correta:")
print(f"   'Melhora ABSURDA de 800% (1→9)'")
print(f"   'Slope POSITIVO = tendência de MELHORA'")
print(f"   'Deveria dizer: ✨ VAI MELHORAR'")
print()
print(f"{'='*80}")
print(f"SOLUÇÃO:")
print(f"{'='*80}")
print()
print(f"Preciso considerar o SINAL do slope:")
print()
print(f"Se slope > 0 (melhora):")
print(f"  → Mesmo com variância alta, é MELHORA")
print(f"  → Prognóstico: ✨ VAI MELHORAR")
print()
print(f"Se slope < 0 (piora):")
print(f"  → Variância alta indica INSTABILIDADE")
print(f"  → Prognóstico: ⚠️ VAI PIORAR")
print()
print(f"Se slope ≈ 0 (estável):")
print(f"  → Mantém nível")
print(f"  → Prognóstico: → MANTÉM\n")
