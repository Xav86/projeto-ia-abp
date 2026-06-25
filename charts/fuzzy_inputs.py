import numpy as np
import matplotlib.pyplot as plt


def _trimf(x, a, b, c):
    y = np.zeros_like(x, dtype=float)
    y = np.where((x > a) & (x <= b), (x - a) / (b - a), y)
    y = np.where((x > b) & (x <= c), (c - x) / (c - b), y)
    y = np.where(x == b, 1.0, y)
    return np.clip(y, 0, 1)


def render_fuzzy_inputs(temp: float, umid: float, vento: float, prob: float = 0.0):
    """Figura com 4 subplots: temperatura, umidade, vento e risco (saída)."""

    fig, axes = plt.subplots(1, 4, figsize=(18, 3.5))
    fig.patch.set_facecolor("none")

    _plot_temperatura(axes[0], temp)
    _plot_umidade(axes[1], umid)
    _plot_vento(axes[2], vento)
    _plot_risco(axes[3], prob)

    fig.tight_layout(pad=2.0)
    return fig


# ── helpers internos ──────────────────────────────────────────────────────────

_STYLE = dict(facecolor="none", tick_params=dict(colors="#555555"))

def _base(ax, title, xlabel):
    ax.set_facecolor("none")
    ax.set_title(title, color="#222222", fontsize=11, pad=8)
    ax.set_xlabel(xlabel, color="#444444", fontsize=9)
    ax.set_ylabel("Pertinência", color="#444444", fontsize=9)
    ax.set_ylim(-0.05, 1.15)
    ax.tick_params(colors="#555555", labelsize=8)
    for spine in ax.spines.values():
        spine.set_edgecolor("#cccccc")
    ax.grid(axis="y", color="#dddddd", linewidth=0.5, linestyle=":")
    ax.legend(facecolor="white", edgecolor="#cccccc", labelcolor="#333333",
              fontsize=8, loc="upper right")


def _vline(ax, val, label):
    ax.axvline(x=val, color="#333333", linewidth=1.6, linestyle="--",
               label=f"Atual ({val:.0f})")


def _plot_temperatura(ax, val):
    x = np.linspace(0, 50, 500)
    curvas = [
        ("Baixa",   _trimf(x,  0,  0, 20), "#4CAF50"),
        ("Média",   _trimf(x, 15, 25, 35), "#FFC107"),
        ("Alta",    _trimf(x, 30, 40, 48), "#FF5722"),
        ("Crítica", _trimf(x, 42, 50, 50), "#B71C1C"),
    ]
    for label, y, cor in curvas:
        ax.plot(x, y, color=cor, linewidth=2, label=label)
        ax.fill_between(x, y, alpha=0.10, color=cor)
    _vline(ax, val, val)
    ax.set_xlim(0, 50)
    _base(ax, "Temperatura (°C)", "°C")


def _plot_umidade(ax, val):
    x = np.linspace(0, 100, 500)
    curvas = [
        ("Crítica", _trimf(x,  0,  0, 20), "#B71C1C"),
        ("Baixa",   _trimf(x, 15, 30, 45), "#FF5722"),
        ("Média",   _trimf(x, 35, 60, 80), "#FFC107"),
        ("Alta",    _trimf(x, 70, 100, 100), "#4CAF50"),
    ]
    for label, y, cor in curvas:
        ax.plot(x, y, color=cor, linewidth=2, label=label)
        ax.fill_between(x, y, alpha=0.10, color=cor)
    _vline(ax, val, val)
    ax.set_xlim(0, 100)
    _base(ax, "Umidade (%)", "%")


def _plot_vento(ax, val):
    x = np.linspace(0, 100, 500)
    curvas = [
        ("Fraco",    _trimf(x,  0,  0, 30), "#4CAF50"),
        ("Moderado", _trimf(x, 20, 45, 70), "#FFC107"),
        ("Forte",    _trimf(x, 60, 80, 95), "#FF5722"),
        ("Crítico",  _trimf(x, 85, 100, 100), "#B71C1C"),
    ]
    for label, y, cor in curvas:
        ax.plot(x, y, color=cor, linewidth=2, label=label)
        ax.fill_between(x, y, alpha=0.10, color=cor)
    _vline(ax, val, val)
    ax.set_xlim(0, 100)
    _base(ax, "Vento (km/h)", "km/h")


def _plot_risco(ax, val: float = 0.0):
    x = np.linspace(0, 100, 500)
    curvas = [
        ("Baixo",   _trimf(x,  0,  0, 30), "#2E7D32"),
        ("Médio",   _trimf(x, 20, 50, 75), "#F9A825"),
        ("Alto",    _trimf(x, 65, 85, 95), "#E64A19"),
        ("Crítico", _trimf(x, 85, 100, 100), "#B71C1C"),
    ]
    for label, y, cor in curvas:
        ax.plot(x, y, color=cor, linewidth=2, label=label)
        ax.fill_between(x, y, alpha=0.10, color=cor)
    _vline(ax, val, val)
    ax.set_xlim(0, 100)
    _base(ax, "Risco — saída (%)", "%")
