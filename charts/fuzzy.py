import numpy as np
import matplotlib.pyplot as plt


def _trapezoidal(x, a, b, c, d):
    """Função de pertinência trapezoidal."""
    y = np.zeros_like(x, dtype=float)
    y = np.where((x >= a) & (x < b),  (x - a) / (b - a), y)
    y = np.where((x >= b) & (x <= c), 1.0,                y)
    y = np.where((x > c) & (x <= d),  (d - x) / (d - c), y)
    return y


def render_fuzzy(valor_atual: float = 72.0):
    """Retorna figura matplotlib com curvas fuzzy e linha do valor atual."""
    x = np.linspace(0, 100, 500)

    curvas = {
        "Baixo":   (_trapezoidal(x,  0,  0, 20, 35), "#2E7D32"),
        "Médio":   (_trapezoidal(x, 20, 35, 50, 65), "#F9A825"),
        "Alto":    (_trapezoidal(x, 50, 65, 75, 85), "#E64A19"),
        "Crítico": (_trapezoidal(x, 75, 88, 100, 100), "#B71C1C"),
    }

    fig, ax = plt.subplots(figsize=(10, 3))
    fig.patch.set_facecolor("none")   # fundo transparente — herda o tema
    ax.set_facecolor("none")

    for label, (y, cor) in curvas.items():
        ax.plot(x, y, color=cor, linewidth=2.5, label=label)
        ax.fill_between(x, y, alpha=0.12, color=cor)

    ax.axvline(
        x=valor_atual,
        color="#555555",
        linewidth=1.8,
        linestyle="--",
        label=f"Valor atual ({valor_atual:.0f}%)",
    )

    ax.set_xlim(0, 100)
    ax.set_ylim(-0.05, 1.15)
    ax.set_xlabel("Risco (%)", color="#444444", fontsize=11)
    ax.set_ylabel("Pertinência", color="#444444", fontsize=11)
    ax.set_title("Funções de Pertinência Fuzzy", color="#222222", fontsize=13, pad=10)

    ax.tick_params(colors="#555555")
    for spine in ax.spines.values():
        spine.set_edgecolor("#cccccc")

    ax.legend(
        facecolor="white",
        edgecolor="#cccccc",
        labelcolor="#333333",
        fontsize=10,
        loc="upper right",
    )

    ax.grid(axis="y", color="#dddddd", linewidth=0.5, linestyle=":")

    fig.tight_layout()
    return fig
