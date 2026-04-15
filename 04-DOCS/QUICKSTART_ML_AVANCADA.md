# ⚡ GUIA RÁPIDO - NOVA PÁGINA ML AVANÇADA

**30 segundos para começar**

---

## 🚀 PASSO 1: Abrir Aplicação

```bash
python gui_escola.py
```

Aguarde ~5 segundos para carregar a interface.

---

## 🤖 PASSO 2: Navegar para Machine Learning

Na **sidebar esquerda**, clique em:

```
🤖  Machine Learning
```

Você verá a nova interface com:
- Cards de modelos
- Botões de treino
- Análise de decisões
- Configuração de pesos

---

## 📊 PASSO 3: Treinar Modelos (Escolha uma opção)

### Opção A: Treinar Tudo (Recomendado Primeira Vez)
```
Clique: 🚀 Treinar Todos os Modelos
├─ Carrega dados
├─ Treina RF_M1 (100 árvores) ~20s
├─ Treina RF_M2 (150 árvores) ~25s
├─ Treina RF_M3 (200 árvores) ~15s
└─ Total: ~60s
```

### Opção B: Treinar Apenas Produção (Rápido)
```
Clique: 📈 Treinar RF_M3 (Produção)
├─ Treina o melhor modelo (94% acurácia)
└─ Total: ~20s
```

### Opção C: Gerar Features Primeiro
```
Clique: 🔄 Gerar Features
├─ Calcula todos os 9 features
├─ Normaliza os dados
└─ Pronto para treino
```

---

## 📈 PASSO 4: Acompanhar Progresso

Você verá na tela:

```
✅ Status: "⏳ Treinando modelos..."

████░░░░░░░░░░░░░░░░░░░░░░░░░░ (35%)
```

**NÃO FECHE A JANELA** - Deixe treinar até 100%

---

## 🎯 PASSO 5: Ver Resultado de Treino

Quando chegar a 100%, aparece **popup** com:

```
📊 RESUMO DE TREINAMENTO

RF_M1
  Acurácia: 83.8%
  F1-Score: 0.834
  Data: 2026-04-14 15:30:00

RF_M2
  Acurácia: 92.5%
  F1-Score: 0.925
  Data: 2026-04-14 15:31:00

RF_M3
  Acurácia: 94.0%
  F1-Score: 0.940
  Data: 2026-04-14 15:32:00
```

Clique **OK** para fechar.

---

## 🔍 PASSO 6: Analisar Decisões do Modelo

Na seção **"ANALISAR DECISÕES DO MODELO"**:

```
1. Abra dropdown "Aluno"
   └─ Escolha um aluno (ex: João Silva)

2. Abra dropdown "Matéria"
   └─ Escolha uma disciplina (ex: Matemática)

3. Clique: 🔍 Analisar
   └─ Aparece análise formatada:

╔═══════════════════════════════════════╗
║ ANÁLISE DE DECISÃO DO MODELO          ║
╚═══════════════════════════════════════╝

📋 INFORMAÇÕES:
  Aluno: João Silva
  Matéria: Matemática
  Série: 7º Fundamental

📊 NOTAS:
  N1: 6.0 → Normalizado: 0.600
  N2: 8.0 → Normalizado: 0.800
  N3: 9.0 → Normalizado: 0.900
  N4: — → —

📈 FEATURES CALCULADAS:
  Média Ponderada: 7.79 (0.779)
  Slope (Tendência): +0.750 (Forte melhora)
  Variância: 0.250 (Consistente)
  Média Geral: 7.2
  % Matérias OK: 85%

🎯 RESULTADO:
  Status Real: Aprovado
  Prognóstico: Vai Melhorar
```
```

---

## ⚖️ PASSO 7: Ajustar Pesos (Opcional)

Na seção **"CONFIGURAR PESOS"**:

```
ANTES (Padrão):
N1: 20%  N2: 25%  N3: 25%  N4: 30%

DEPOIS (Customizado):
N1: 15%  N2: 25%  N3: 25%  N4: 35%
    ↑                            ↑
   menos importante         mais importante
```

**Para mudar:**
1. Arraste os **sliders** para novas posições
2. Veja percentagem atualizar em tempo real
3. Clique **🔄 Gerar Features** para aplicar
4. Treine novamente se quiser refletir as mudanças

---

## 💡 DICAS & TROUBLESHOOTING

### Se ficar lento/travado
- Feche outras abas do sistema
- Não mexa na janela durante treino
- Aguarde barra chegar a 100%

### Se não encontrar alunos
- Clique **🔄 Gerar Features** primeiro
- Você precisa ter dados no banco (`escola.db`)

### Se modelo não treina
- Verifique se `ml_dataset.csv` foi criado
- Veja se `requirements.txt` está instalado:
  ```bash
  pip install -r requirements.txt
  ```

### Para resets completo
```bash
# Apaga modelos antigos
rm ml_models/*.pkl ml_models/*.json

# Regenera e treina
python train_simple.py
```

---

## ⏱️ TEMPO ESPERADO

| Operação | Tempo |
|----------|-------|
| Abrir app | 2-3s |
| Gerar Features (100 alunos) | 5s |
| Treinar RF_M3 | 20s |
| Treinar RF_M1 + RF_M2 + RF_M3 | 60s |
| Analisar decisão | <1s |
| Ajustar peso + regenerar | 5s |

---

## 🎯 O QUE CADA BOTÃO FAZ

| Botão | Ação |
|-------|------|
| 🔄 Gerar Features | Calcula 9 features ML de todo dataset |
| 🚀 Treinar Todos | Treina 3 modelos sequencialmente |
| 📈 Treinar RF_M3 | Treina apenas modelo de produção |
| 🔍 Analisar | Mostra como modelo decidiu para 1 aluno |

---

## 📊 EXEMPLO PRÁTICO

**Cenário:** Você tem João em Matemática com N1=2, N2=5

### Sem Dados de N3/N4

**Sistema faz:**
1. Calcula slope: (5-2)/2 = 150% (melhora!)
2. Passa para modelo RF_M3
3. Modelo diz: "Status vai ser Aprovado"
4. Exibe: **[*] Vai Melhorar**

### Com Dados de N3/N4 (João tirou N3=8, N4=8)

**Sistema faz:**
1. Compara: Modelo previa melhora, obteve 8.0?
2. Resultado real: Aprovado (8+8=16 média)
3. Previsão: Tinha previsto Aprovado também
4. Exibe: **[ok] como esperado**

---

## 🔗 DOCUMENTAÇÃO COMPLETA

Para entender **TUDO** sobre ML:
```
Leia: DOCUMENTACAO_CALCULOS.md
├─ 9 Features explicadas
├─ Fórmulas de Slope e Variância
├─ Como funciona o treino
├─ Interpretação de prognósticos
└─ Exemplo completo walkthrough
```

Para entender **ARQUITETURA**:
```
Leia: ESTRUTURA_PROJETO.md
├─ Organização de arquivos
├─ Fluxo de dependências
├─ Como adicionar módulos
└─ Checklist de manutenção
```

---

## ✅ CHECKLIST PRIMEIRO USO

- [ ] Abrir `gui_escola.py`
- [ ] Navegar para 🤖 Machine Learning
- [ ] Clicar "🔄 Gerar Features" (aguarde 5s)
- [ ] Clicar "🚀 Treinar Todos" (aguarde 60s)
- [ ] Ver popup com resultados
- [ ] Tentar "🔍 Analisar" um aluno+matéria
- [ ] Ajustar pesos com sliders
- [ ] Ler `DOCUMENTACAO_CALCULOS.md`

---

## 🎉 PRONTO!

Você está pronto para:
- ✅ Treinar modelos de ML
- ✅ Analisar decisões do modelo
- ✅ Configurar pesos personalizados
- ✅ Ver análise visual de cada aluno

**Divirta-se explorando! 🚀**

---

**Tempo de leitura:** 5 minutos  
**Tempo para primeiro treino:** ~5 minutos  
**Status:** ✅ Tudo pronto para uso!
