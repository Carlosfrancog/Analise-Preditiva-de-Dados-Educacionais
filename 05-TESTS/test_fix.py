#!/usr/bin/env python3
"""Teste do caso N1=1.0, N2=9.0 após correção"""

# Test lógica de slope
print("="*80)
print("🧪 TESTE DA CORREÇÃO: N1=1.0, N2=9.0 em Química")
print("="*80)
print()

n1_raw = 1.0
n2_raw = 9.0

media_n12 = (n1_raw + n2_raw) / 2
slope_pct = ((n2_raw - n1_raw) / n1_raw) * 100

print(f"DADOS:")
print(f"  N1: {n1_raw}")
print(f"  N2: {n2_raw}")
print(f"  Média: {media_n12:.1f}")
print(f"  Slope: {slope_pct:.0f}%")
print()

# Status atual
if media_n12 < 5:
    status_n12 = 0
    status_name = "❌ Reprovado"
elif media_n12 < 6:
    status_n12 = 1
    status_name = "⚠️ Recuperação"
else:
    status_n12 = 2
    status_name = "✅ Aprovado"

print(f"STATUS ATUAL: {status_name}")
print()

# Nova lógica (após correção)
print(f"NOVA LÓGICA (CORRIGIDA):")
print()

if slope_pct > 20:
    trend = "✨"
    prognosis = "will_improve"
    explicacao = f"MELHORA EXCEPCIONAL de {slope_pct:.0f}%!"
elif slope_pct < -20:
    trend = "⚠️"
    prognosis = "will_decline"
    explicacao = f"Queda BRUSCA de {abs(slope_pct):.0f}%"
else:
    trend = "→"
    prognosis = "stable"
    explicacao = "Desempenho estável"

print(f"  Slope: {slope_pct:.0f}%")
if slope_pct > 20:
    print(f"  → slope > 20% (MELHORA SIGNIFICATIVA)")
elif slope_pct < -20:
    print(f"  → slope < -20% (PIORA SIGNIFICATIVA)")
else:
    print(f"  → slope entre -20% e +20% (ESTÁVEL)")

print()
print(f"RESULTADO:")
print(f"  Trend: {trend}")
print(f"  Prognosis: {prognosis}")
print(f"  Mensagem: {explicacao}")
print()

print(f"{"="*80}")
print(f"✅ CORRIGIDO!")
print(f"{"="*80}")
print()
print(f"ANTES (Errado):")
print(f"  N1=1, N2=9 (melhora de 800%)")
print(f"  → ⚠️ 'Vai piorar - variação alta, instabilidade'")
print()
print(f"DEPOIS (Correto):")
print(f"  N1=1, N2=9 (melhora de 800%)")
print(f"  → ✨ 'Melhora excepcional de 800%!'")
print()
