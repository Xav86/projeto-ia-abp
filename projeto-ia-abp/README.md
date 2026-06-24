# 🔥 Sistema Inteligente de Previsão de Incêndios Florestais

Interface web desenvolvida com **Streamlit** para um sistema de previsão de risco de incêndios florestais baseado em **Lógica Fuzzy**.

## Objetivo

Fornecer uma interface visual interativa que receberá dados climáticos do usuário e exibirá o nível de risco calculado por um motor de inferência fuzzy.

## Estrutura do projeto

```
projeto-ia-abp/
├── app.py                        # Arquivo principal da aplicação
├── requirements.txt              # Dependências Python
├── config/
│   └── defaults.json             # Valores padrão exibidos antes do cálculo da IA
├── components/
│   └── fuzzy_engine.py           # Ponto de integração com o motor fuzzy (a implementar)
├── charts/
│   ├── gauge.py                  # Gauge de risco (Plotly)
│   └── fuzzy.py                  # Gráfico de pertinência fuzzy (Matplotlib)
└── assets/                       # Recursos estáticos (imagens, ícones)
```

## Funcionalidades

- Entrada de parâmetros climáticos via sliders (temperatura, umidade, vento)
- Indicador visual tipo velocímetro com faixas de risco
- Gráfico de funções de pertinência fuzzy com marcação do valor atual
- Seção de justificativa textual do resultado
- Layout em duas colunas adaptado para visualização sem scroll

## Como executar

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Tecnologias

| Biblioteca   | Uso                              |
|--------------|----------------------------------|
| Streamlit    | Interface web                    |
| Plotly       | Gauge (velocímetro de risco)     |
| Matplotlib   | Gráfico de pertinência fuzzy     |
| NumPy        | Cálculo das funções trapezoidais |

## Integração com a IA (próxima etapa)

O arquivo `components/fuzzy_engine.py` contém a função `calcular_risco`, que receberá os valores climáticos e deverá retornar um dicionário com:

```python
{
    "risco":         str,   # "Baixo" | "Médio" | "Alto" | "Crítico"
    "probabilidade": float, # 0.0 a 100.0
    "justificativa": str    # Texto explicativo gerado pelo motor fuzzy
}
```

Enquanto a função retornar `None`, a interface exibe os valores definidos em `config/defaults.json`.
