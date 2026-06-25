import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


# ── Variáveis de entrada ────────────────────────────────────────────────────

temperatura = ctrl.Antecedent(np.arange(0, 51, 1), "temperatura")
umidade     = ctrl.Antecedent(np.arange(0, 101, 1), "umidade")
vento       = ctrl.Antecedent(np.arange(0, 101, 1), "vento")

# ── Variável de saída ───────────────────────────────────────────────────────

risco = ctrl.Consequent(np.arange(0, 101, 1), "risco")

# ── Funções de pertinência: Temperatura (°C) ────────────────────────────────

temperatura["baixa"]   = fuzz.trimf(temperatura.universe, [0,  0,  20])
temperatura["media"]   = fuzz.trimf(temperatura.universe, [15, 25, 35])
temperatura["alta"]    = fuzz.trimf(temperatura.universe, [30, 40, 48])
temperatura["critica"] = fuzz.trimf(temperatura.universe, [42, 50, 50])

# ── Funções de pertinência: Umidade (%) ─────────────────────────────────────
# Quanto menor a umidade, maior o risco — por isso "critica" está na faixa mais baixa

umidade["critica"] = fuzz.trimf(umidade.universe, [0,  0,  20])
umidade["baixa"]   = fuzz.trimf(umidade.universe, [15, 30, 45])
umidade["media"]   = fuzz.trimf(umidade.universe, [35, 60, 80])
umidade["alta"]    = fuzz.trimf(umidade.universe, [70, 100, 100])

# ── Funções de pertinência: Vento (km/h, 0–100) ─────────────────────────────

vento["fraco"]    = fuzz.trimf(vento.universe,  [0,  0,  30])
vento["moderado"] = fuzz.trimf(vento.universe,  [20, 45, 70])
vento["forte"]    = fuzz.trimf(vento.universe,  [60, 80, 95])
vento["critico"]  = fuzz.trimf(vento.universe,  [85, 100, 100])

# ── Funções de pertinência: Risco (saída 0–100%) ────────────────────────────

risco["baixo"]   = fuzz.trimf(risco.universe, [0,  0,  30])
risco["medio"]   = fuzz.trimf(risco.universe, [20, 50, 75])
risco["alto"]    = fuzz.trimf(risco.universe, [65, 85, 95])
risco["critico"] = fuzz.trimf(risco.universe, [85, 100, 100])

# ── Regras fuzzy (24 regras) ────────────────────────────────────────────────
#
# Risco CRÍTICO: exige temperatura alta ou crítica — frio nunca gera crítico
# Risco ALTO:   combinações de calor + seca ou vento intenso
# Risco MÉDIO:  condições moderadas ou frio com vento
# Risco BAIXO:  temperatura baixa ou umidade alta

regras = [
    # --- Crítico (6 regras) ---
    ctrl.Rule(temperatura["critica"] & umidade["critica"],                          risco["critico"]),
    ctrl.Rule(temperatura["critica"] & vento["critico"],                            risco["critico"]),
    ctrl.Rule(temperatura["alta"]    & umidade["critica"] & vento["forte"],         risco["critico"]),
    ctrl.Rule(temperatura["alta"]    & umidade["critica"] & vento["critico"],       risco["critico"]),
    ctrl.Rule(temperatura["critica"] & umidade["baixa"]   & vento["forte"],         risco["critico"]),
    ctrl.Rule(temperatura["alta"]    & umidade["baixa"]   & vento["critico"],       risco["critico"]),

    # --- Alto (7 regras) ---
    ctrl.Rule(temperatura["alta"]    & umidade["critica"],                          risco["alto"]),   # cobre alta+critica sem vento forte
    ctrl.Rule(temperatura["alta"]    & umidade["baixa"],                            risco["alto"]),
    ctrl.Rule(temperatura["alta"]    & vento["forte"],                              risco["alto"]),
    ctrl.Rule(temperatura["media"]   & umidade["critica"],                          risco["alto"]),
    ctrl.Rule(temperatura["critica"] & umidade["media"],                            risco["alto"]),
    ctrl.Rule(temperatura["critica"] & umidade["baixa"],                            risco["alto"]),   # cobre critica+baixa sem vento forte
    ctrl.Rule(temperatura["media"]   & vento["critico"] & umidade["baixa"],         risco["alto"]),  # temp media + vento extremo + seco

    # --- Médio (7 regras) ---
    ctrl.Rule(temperatura["media"]   & umidade["media"],                            risco["medio"]),
    ctrl.Rule(temperatura["media"]   & umidade["baixa"],                            risco["medio"]),  # cobre media+baixa
    ctrl.Rule(temperatura["alta"]    & umidade["media"],                            risco["medio"]),  # cobre alta+media
    ctrl.Rule(temperatura["alta"]    & umidade["alta"],                             risco["medio"]),
    ctrl.Rule(temperatura["critica"] & umidade["alta"],                             risco["medio"]),  # calor extremo com umidade alta
    ctrl.Rule(temperatura["baixa"]   & vento["forte"],                              risco["medio"]),
    ctrl.Rule(temperatura["baixa"]   & vento["critico"],                            risco["medio"]),  # frio + vento extremo

    # --- Baixo (4 regras) ---
    ctrl.Rule(temperatura["baixa"]   & umidade["alta"],                             risco["baixo"]),
    ctrl.Rule(temperatura["media"]   & umidade["alta"],                             risco["baixo"]),
    ctrl.Rule(temperatura["baixa"]   & vento["fraco"],                              risco["baixo"]),
    ctrl.Rule(temperatura["baixa"]   & vento["moderado"],                           risco["baixo"]),
]

sistema = ctrl.ControlSystem(regras)


# ── Helpers para justificativa semântica ────────────────────────────────────

def _cat_temperatura(t):
    if t <= 15:   return "baixa"
    if t <= 30:   return "média"
    if t <= 42:   return "alta"
    return "crítica"

def _cat_umidade(u):
    if u <= 15:   return "crítica"
    if u <= 35:   return "baixa"
    if u <= 65:   return "média"
    return "alta"

def _cat_vento(v):
    if v <= 20:  return "fraco"
    if v <= 55:  return "moderado"
    if v <= 82:  return "forte"
    return "crítico"

def _justificativa(t, u, v, classificacao):
    ct = _cat_temperatura(t)
    cu = _cat_umidade(u)
    cv = _cat_vento(v)

    partes = []

    if ct in ("alta", "crítica"):
        partes.append(f"temperatura {ct} ({t}°C) favorece o ressecamento da vegetação")
    else:
        partes.append(f"temperatura {ct} ({t}°C) reduz o risco de ignição")

    if cu in ("crítica", "baixa"):
        partes.append(f"umidade {cu} ({u}%) aumenta a inflamabilidade do ambiente")
    else:
        partes.append(f"umidade {cu} ({u}%) contribui para reduzir o risco")

    if cv in ("forte", "crítico"):
        partes.append(f"vento {cv} ({v} km/h) acelera a propagação das chamas")
    else:
        partes.append(f"vento {cv} ({v} km/h) tem baixo impacto na propagação")

    corpo = "; ".join(partes).capitalize()
    return f"{corpo}. Risco classificado como {classificacao}."


# ── Função de integração ────────────────────────────────────────────────────

def calcular_risco(temperatura_valor: float, umidade_valor: float, vento_valor: float):
    simulacao = ctrl.ControlSystemSimulation(sistema)
    simulacao.input["temperatura"] = temperatura_valor
    simulacao.input["umidade"]     = umidade_valor
    simulacao.input["vento"]       = vento_valor
    simulacao.compute()

    valor = simulacao.output.get("risco", 25.0)

    if valor < 30:
        classificacao = "Baixo"
    elif valor < 60:
        classificacao = "Médio"
    elif valor < 85:
        classificacao = "Alto"
    else:
        classificacao = "Crítico"

    return {
        "risco":         classificacao,
        "probabilidade": round(float(valor), 1),
        "justificativa": _justificativa(temperatura_valor, umidade_valor, vento_valor, classificacao),
    }
