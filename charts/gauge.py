import plotly.graph_objects as go


def render_gauge(valor: float) -> go.Figure:
    """Renderiza gauge de risco (0–100). Faixas: Baixo/Médio/Alto/Crítico."""
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=valor,
            number={"suffix": "%", "font": {"size": 36, "color": "#333333"}},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1},
                "bar": {"color": "#333333", "thickness": 0.25},
                "steps": [
                    {"range": [0, 30],  "color": "#4CAF50"},  # Baixo
                    {"range": [30, 60], "color": "#FFC107"},  # Médio
                    {"range": [60, 85], "color": "#FF5722"},  # Alto
                    {"range": [85, 100],"color": "#B71C1C"},  # Crítico
                ],
                "threshold": {
                    "line": {"color": "#111111", "width": 4},
                    "thickness": 0.8,
                    "value": valor,
                },
            },
        )
    )

    fig.update_layout(
        annotations=[
            dict(x=0.27,  y=0.05, text="Baixo",   showarrow=False, font=dict(size=12, color="#4CAF50")),
            dict(x=0.43,  y=0.50, text="Médio",   showarrow=False, font=dict(size=12, color="#FFC107")),
            dict(x=0.58,  y=0.50, text="Alto",    showarrow=False, font=dict(size=12, color="#FF5722")),
            dict(x=0.73,  y=0.05, text="Crítico", showarrow=False, font=dict(size=12, color="#B71C1C")),
        ],
        margin=dict(t=10, b=0, l=20, r=20),
        height=220,
        paper_bgcolor="rgba(0,0,0,0)",
        font={"color": "#333333"},
    )

    return fig
