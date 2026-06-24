# Relatório Técnico — Sistema Inteligente de Previsão de Incêndios Florestais

**Disciplina:** Inteligência Artificial — Projeto ABP  
**Data:** junho de 2026

---

## 1. Visão Geral

O sistema implementa um motor de inferência fuzzy do tipo **Mamdani** para estimar o risco de incêndio florestal a partir de três variáveis climáticas de entrada. A saída é um valor numérico contínuo (0–100%) defuzzificado pelo **método do centroide**, classificado em quatro categorias.

A interface foi desenvolvida em **Streamlit**, com layout em duas colunas mostrando os controles de entrada, um gauge visual tipo velocímetro, o gráfico de funções de pertinência e uma justificativa textual gerada automaticamente.

---

## 2. Variáveis de Entrada

### 2.1 Temperatura (°C) — universo: 0 a 50

| Conjunto | Função | Parâmetros |
|----------|--------|------------|
| Baixa    | Triangular | [0, 0, 20] — cobre frio; pico em 0°C |
| Média    | Triangular | [15, 25, 35] — pico em 25°C |
| Alta     | Triangular | [30, 40, 48] — pico em 40°C |
| Crítica  | Triangular | [42, 50, 50] — pico em 50°C |

> Sobreposição intencional entre conjuntos (ex.: 15–20°C é simultaneamente baixa e média) garante transições suaves.

### 2.2 Umidade Relativa (%) — universo: 0 a 100

| Conjunto | Função | Parâmetros |
|----------|--------|------------|
| Crítica  | Triangular | [0, 0, 20] — ar muito seco |
| Baixa    | Triangular | [15, 30, 45] |
| Média    | Triangular | [35, 60, 80] |
| Alta     | Triangular | [70, 100, 100] — ar úmido |

> Nomenclatura invertida em relação ao risco: umidade "crítica" (0–20%) representa o cenário de **maior** perigo.

### 2.3 Velocidade do Vento (km/h) — universo: 0 a 100

| Conjunto | Função | Parâmetros |
|----------|--------|------------|
| Fraco    | Triangular | [0, 0, 30] |
| Moderado | Triangular | [20, 45, 70] |
| Forte    | Triangular | [60, 80, 95] |
| Crítico  | Triangular | [85, 100, 100] |

---

## 3. Variável de Saída — Risco (%)

| Conjunto | Função | Parâmetros | Faixa de classificação |
|----------|--------|------------|------------------------|
| Baixo    | Triangular | [0, 0, 30]    | saída < 30%   |
| Médio    | Triangular | [20, 50, 75]  | 30% ≤ saída < 60% |
| Alto     | Triangular | [65, 85, 95]  | 60% ≤ saída < 85% |
| Crítico  | Triangular | [85, 100, 100]| saída ≥ 85%   |

---

## 4. Regras Fuzzy (22 regras)

### Crítico (5 regras) — exige temperatura alta ou crítica

| # | Condição | Consequente |
|---|----------|-------------|
| 1 | Temperatura **Crítica** AND Umidade **Crítica** | Risco **Crítico** |
| 2 | Temperatura **Crítica** AND Vento **Crítico** | Risco **Crítico** |
| 3 | Temperatura **Alta** AND Umidade **Crítica** AND Vento **Forte** | Risco **Crítico** |
| 4 | Temperatura **Alta** AND Umidade **Crítica** AND Vento **Crítico** | Risco **Crítico** |
| 5 | Temperatura **Crítica** AND Umidade **Baixa** AND Vento **Forte** | Risco **Crítico** |

### Alto (7 regras)

| # | Condição | Consequente |
|---|----------|-------------|
| 6 | Temperatura **Alta** AND Umidade **Crítica** | Risco **Alto** |
| 7 | Temperatura **Alta** AND Umidade **Baixa** | Risco **Alto** |
| 8 | Temperatura **Alta** AND Vento **Forte** | Risco **Alto** |
| 9 | Temperatura **Média** AND Umidade **Crítica** | Risco **Alto** |
| 10 | Temperatura **Crítica** AND Umidade **Média** | Risco **Alto** |
| 11 | Temperatura **Crítica** AND Umidade **Baixa** | Risco **Alto** |
| 12 | Vento **Crítico** AND Umidade **Baixa** | Risco **Alto** |

### Médio (6 regras)

| # | Condição | Consequente |
|---|----------|-------------|
| 13 | Temperatura **Média** AND Umidade **Média** | Risco **Médio** |
| 14 | Temperatura **Média** AND Umidade **Baixa** | Risco **Médio** |
| 15 | Temperatura **Alta** AND Umidade **Média** | Risco **Médio** |
| 16 | Temperatura **Alta** AND Umidade **Alta** | Risco **Médio** |
| 17 | Temperatura **Crítica** AND Umidade **Alta** | Risco **Médio** |
| 18 | Temperatura **Baixa** AND Vento **Forte** | Risco **Médio** |

### Baixo (4 regras)

| # | Condição | Consequente |
|---|----------|-------------|
| 19 | Temperatura **Baixa** AND Umidade **Alta** | Risco **Baixo** |
| 20 | Temperatura **Média** AND Umidade **Alta** | Risco **Baixo** |
| 21 | Temperatura **Baixa** AND Vento **Fraco** | Risco **Baixo** |
| 22 | Temperatura **Baixa** AND Vento **Moderado** | Risco **Baixo** |

---

## 5. Comparação com o Notebook de Referência (Colab)

O notebook de referência utilizava **16 regras** cobrindo os principais cenários. O sistema implementado mantém todas as 16 regras originais e adiciona **6 regras complementares** para eliminar lacunas de cobertura identificadas durante os testes.

| Aspecto | Notebook Colab | Sistema implementado |
|---------|---------------|----------------------|
| Número de regras | 16 | 22 (16 originais + 6 cobertura) |
| Range de temperatura | 0–50°C | 0–50°C ✓ |
| Range de umidade | 0–100% | 0–100% ✓ |
| Range de vento | 0–100 km/h | 0–100 km/h ✓ |
| Método de inferência | Mamdani | Mamdani ✓ |
| Defuzzificação | Centroide | Centroide ✓ |
| Funções de pertinência | Triangulares | Triangulares ✓ |
| Parâmetros das MFs | Alinhados | Alinhados ✓ |

**Regras adicionadas em relação ao Colab (lacunas de cobertura):**

- Regra 6: `Alta + Crítica → Alto` — cobre temperatura alta com umidade crítica e vento fraco/moderado
- Regra 11: `Crítica + Baixa → Alto` — cobre temperatura crítica com umidade baixa e vento fraco/moderado
- Regra 14: `Média + Baixa → Médio` — cobre temperatura média com umidade baixa
- Regra 15: `Alta + Média → Médio` — cobre temperatura alta com umidade média
- Regra 17: `Crítica + Alta → Médio` — cobre temperatura extrema com umidade alta (atenuante)
- Regra 18 (era 17 original): `Baixa + Moderado → Baixo` — mantida do notebook

Sem essas regras complementares, combinações como 35°C + 0% de umidade + vento fraco retornavam indevidamente "Baixo" porque nenhuma regra era ativada e o sistema retornava o valor padrão.

---

## 6. Exemplos com Resultados Esperados

Os valores de saída variam continuamente; os abaixo são estimativas baseadas na análise das ativações das regras.

### Exemplo 1 — Dia de outono típico (Baixo risco)

| Entrada | Valor | Classificação fuzzy dominante |
|---------|-------|-------------------------------|
| Temperatura | 15°C | Baixa / Média (transição) |
| Umidade | 80% | Alta |
| Vento | 10 km/h | Fraco |

**Regras ativas:** Média+Alta→Baixo (forte), Baixa+Alta→Baixo, Baixa+Fraco→Baixo  
**Saída esperada:** ~10–20% → **Baixo**  
**Justificativa:** Temperatura amena, alta umidade e vento fraco criam condições muito seguras. Vegetação úmida não sustenta ignição.

---

### Exemplo 2 — Primavera seca com vento moderado (Médio risco)

| Entrada | Valor | Classificação fuzzy dominante |
|---------|-------|-------------------------------|
| Temperatura | 28°C | Média |
| Umidade | 30% | Baixa |
| Vento | 25 km/h | Moderado |

**Regras ativas:** Média+Baixa→Médio (dominante)  
**Saída esperada:** ~45–55% → **Médio**  
**Justificativa:** Temperatura moderada com umidade baixa cria risco intermediário. Vento moderado contribui mas não domina.

---

### Exemplo 3 — Tarde de verão quente e seca (Alto risco)

| Entrada | Valor | Classificação fuzzy dominante |
|---------|-------|-------------------------------|
| Temperatura | 38°C | Alta |
| Umidade | 20% | Crítica (transição para Baixa) |
| Vento | 30 km/h | Moderado |

**Regras ativas:** Alta+Crítica→Alto (nova regra 6), Alta+Baixa→Alto  
**Saída esperada:** ~70–78% → **Alto**  
**Justificativa:** Temperatura alta combinada com umidade próxima do crítico representa risco elevado de ignição. Vento moderado aumenta a propagação.

---

### Exemplo 4 — Onda de calor extrema com ressecamento (Crítico)

| Entrada | Valor | Classificação fuzzy dominante |
|---------|-------|-------------------------------|
| Temperatura | 45°C | Alta (transição para Crítica) |
| Umidade | 5% | Crítica |
| Vento | 90 km/h | Forte/Crítico |

**Regras ativas:** Crítica+Crítica→Crítico, Crítica+VentoCrítico→Crítico, Alta+Crítica+Forte→Crítico, Alta+Crítica+Crítico→Crítico  
**Saída esperada:** ~88–95% → **Crítico**  
**Justificativa:** Múltiplas regras de máxima severidade ativadas simultaneamente. Condição de catástrofe iminente.

---

### Exemplo 5 — Inverno anômalo: frio com vento muito forte (Médio)

| Entrada | Valor | Classificação fuzzy dominante |
|---------|-------|-------------------------------|
| Temperatura | 10°C | Baixa |
| Umidade | 15% | Crítica (transição) |
| Vento | 70 km/h | Forte |

**Regras ativas:** Baixa+Forte→Médio  
**Saída esperada:** ~40–50% → **Médio**  
**Justificativa:** Mesmo com temperatura baixa, vento forte pode propagar fagulhas e ressecar vegetação. Risco médio é adequado para a situação.

---

### Exemplo 6 — Calor extremo com chuva recente (Médio)

| Entrada | Valor | Classificação fuzzy dominante |
|---------|-------|-------------------------------|
| Temperatura | 48°C | Crítica |
| Umidade | 85% | Alta |
| Vento | 20 km/h | Fraco |

**Regras ativas:** Crítica+Alta→Médio (nova regra 17)  
**Saída esperada:** ~40–55% → **Médio**  
**Justificativa:** Temperatura extrema, porém umidade muito alta inibe a ignição. O sistema reconhece o calor mas pondera o efeito protetor da umidade.

---

## 7. Arquitetura do Sistema

```
app.py (Streamlit)
  │
  ├── sliders → temperatura, umidade, vento
  │
  ├── [botão Calcular Risco]
  │       └── calcular_risco(t, u, v) → components/fuzzy_engine.py
  │               ├── ControlSystemSimulation (scikit-fuzzy)
  │               ├── compute() → defuzzificação centroide
  │               └── retorna { risco, probabilidade, justificativa }
  │
  ├── st.session_state → armazena resultado entre reruns
  │
  ├── render_gauge(probabilidade) → charts/gauge.py (Plotly)
  └── render_fuzzy(probabilidade) → charts/fuzzy.py (Matplotlib)
```

---

## 8. Decisões de Projeto Relevantes

**Por que 22 regras e não as 16 do Colab?**  
O conjunto de 16 regras do notebook deixava lacunas — combinações de entrada que não ativavam nenhuma regra. Nesses casos, o scikit-fuzzy retorna um output indefinido e o sistema usava um fallback de 25% (Baixo), que é semanticamente incorreto para cenários como 40°C + 50% de umidade. As 6 regras adicionais fecham essas lacunas sem contradizer as originais.

**Por que a umidade "Crítica" representa baixa umidade?**  
A convenção do Colab de referência nomeia os conjuntos pelo nível de perigo, não pelo valor físico. Umidade crítica = ar seco = mais inflamável. Isso é mantido para consistência com o notebook.

**Por que o gráfico fuzzy mostra a variável de saída (Risco) e não as entradas?**  
A escolha segue o padrão adotado no notebook de referência para visualização do resultado. Uma extensão possível é exibir as curvas das três entradas com a pertinência atual marcada.

**Thresholds de classificação alinhados entre engine e gauge:**  
O gauge visual usa exatamente os mesmos limites do engine (30 / 60 / 85) para evitar inconsistências visuais onde um valor de 82% exibiria "Crítico" no velocímetro mas seria classificado como "Alto" pelo motor.
