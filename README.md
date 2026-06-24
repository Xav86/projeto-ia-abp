# Sistema Inteligente de Previsão de Incêndios Florestais

Interface web desenvolvida com **Streamlit** para um sistema de previsão de risco de incêndios florestais baseado em **Lógica Fuzzy (Mamdani)**.

## Objetivo

Fornecer uma interface visual interativa que recebe dados climáticos do usuário e exibe o nível de risco calculado por um motor de inferência fuzzy, com justificativa textual e indicadores visuais.

## Estrutura do projeto

```
projeto-ia-abp/
├── app.py                        # Aplicação principal Streamlit
├── requirements.txt              # Dependências Python
├── relatorio.md                  # Relatório técnico do sistema
├── config/
│   └── defaults.json             # Valores exibidos antes do primeiro cálculo
├── components/
│   └── fuzzy_engine.py           # Motor de inferência fuzzy (scikit-fuzzy)
├── charts/
│   ├── gauge.py                  # Gauge de risco (Plotly)
│   └── fuzzy.py                  # Gráfico de pertinência fuzzy (Matplotlib)
├── tests/
│   └── test_engine.py            # Bateria de testes do motor fuzzy
└── assets/                       # Recursos estáticos
```

## Funcionalidades

- Entrada de parâmetros climáticos via sliders (temperatura, umidade, velocidade do vento)
- Inferência fuzzy Mamdani com 22 regras e defuzzificação por centroide
- Indicador visual tipo velocímetro com faixas de risco coloridas
- Gráfico de funções de pertinência fuzzy com marcação do valor atual
- Justificativa textual gerada semanticamente a partir das classificações de entrada
- Layout em duas colunas adaptado para visualização sem scroll

## Como executar

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Como testar a lógica fuzzy

```bash
python tests/test_engine.py
```

Executa 20 verificações automáticas: 17 cenários com classificação esperada (Baixo / Médio / Alto / Crítico) e 3 testes de monotonicidade que garantem que vento crescente nunca reduz o risco calculado.

## Tecnologias

| Biblioteca    | Versão mínima | Uso                                        |
|---------------|---------------|--------------------------------------------|
| Streamlit     | 1.35.0        | Interface web                              |
| Plotly        | 5.20.0        | Gauge (velocímetro de risco)               |
| Matplotlib    | 3.8.0         | Gráfico de pertinência fuzzy               |
| NumPy         | 1.26.0        | Universos e funções de pertinência         |
| scikit-fuzzy  | 0.4.2         | Motor de inferência fuzzy (Mamdani)        |
| SciPy         | 1.11.0        | Dependência do scikit-fuzzy                |
| NetworkX      | 3.2.0         | Dependência do scikit-fuzzy                |

## Variáveis e classificações

| Variável      | Range    | Conjuntos fuzzy                            |
|---------------|----------|--------------------------------------------|
| Temperatura   | 0–50 °C  | Baixa / Média / Alta / Crítica             |
| Umidade       | 0–100 %  | Crítica / Baixa / Média / Alta             |
| Vento         | 0–100 km/h | Fraco / Moderado / Forte / Crítico       |
| **Risco**     | 0–100 %  | Baixo (<30) / Médio (30–60) / Alto (60–85) / Crítico (≥85) |

## Motor fuzzy

O motor utiliza **22 regras** (5 Crítico + 7 Alto + 6 Médio + 4 Baixo) com inferência Mamdani e defuzzificação por centroide. Consulte `relatorio.md` para detalhes completos das regras, exemplos esperados e comparação com o notebook de referência.
