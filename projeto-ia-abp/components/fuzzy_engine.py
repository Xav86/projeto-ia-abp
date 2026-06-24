import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


# Entradas
temperatura = ctrl.Antecedent(
    np.arange(0, 51, 1),
    "temperatura"
)

umidade = ctrl.Antecedent(
    np.arange(0, 101, 1),
    "umidade"
)

vento = ctrl.Antecedent(
    np.arange(0, 151, 1),
    "vento"
)


# Saída
risco = ctrl.Consequent(
    np.arange(0, 101, 1),
    "risco"
)


# Funções de pertinência - temperatura
temperatura["baixa"] = fuzz.trapmf(
    temperatura.universe,
    [0, 0, 15, 25]
)

temperatura["media"] = fuzz.trimf(
    temperatura.universe,
    [20, 30, 40]
)

temperatura["alta"] = fuzz.trapmf(
    temperatura.universe,
    [30, 35, 50, 50]
)


# Umidade
umidade["baixa"] = fuzz.trapmf(
    umidade.universe,
    [0, 0, 30, 45]
)

umidade["media"] = fuzz.trimf(
    umidade.universe,
    [30, 50, 70]
)

umidade["alta"] = fuzz.trapmf(
    umidade.universe,
    [60, 80, 100, 100]
)


# Vento
vento["fraco"] = fuzz.trapmf(
    vento.universe,
    [0, 0, 10, 30]
)

vento["medio"] = fuzz.trimf(
    vento.universe,
    [20, 50, 80]
)

vento["forte"] = fuzz.trapmf(
    vento.universe,
    [60, 80, 150, 150]
)


# Risco final
risco["baixo"] = fuzz.trapmf(
    risco.universe,
    [0, 0, 20, 35]
)

risco["medio"] = fuzz.trimf(
    risco.universe,
    [25, 50, 65]
)

risco["alto"] = fuzz.trimf(
    risco.universe,
    [50, 70, 85]
)

risco["critico"] = fuzz.trapmf(
    risco.universe,
    [75, 90, 100, 100]
)


# Regras fuzzy
regras = [


    ctrl.Rule(
    temperatura["alta"] &
    umidade["baixa"],
    risco["alto"]
),

ctrl.Rule(
    temperatura["alta"] &
    vento["forte"],
    risco["critico"]
),

ctrl.Rule(
    umidade["baixa"] &
    vento["forte"],
    risco["critico"]
), 

    ctrl.Rule(
        temperatura["alta"] &
        umidade["baixa"] &
        vento["forte"],
        risco["critico"]
    ),

    ctrl.Rule(
        temperatura["alta"] &
        umidade["baixa"],
        risco["alto"]
    ),

    ctrl.Rule(
        temperatura["media"] &
        umidade["media"] &
        vento["medio"],
        risco["medio"]
    ),

    ctrl.Rule(
        temperatura["baixa"] &
        umidade["alta"],
        risco["baixo"]
    ),
    
    ctrl.Rule(
         temperatura["alta"] &
         umidade["baixa"],
         risco["alto"]
    ),
    
    ctrl.Rule(
        temperatura["alta"] &
        vento["medio"],
     risco["alto"]
    ),

]


sistema = ctrl.ControlSystem(regras)


def calcular_risco(
    temperatura_valor: float,
    umidade_valor: float,
    vento_valor: float
):

    simulacao = ctrl.ControlSystemSimulation(sistema)

    simulacao.input["temperatura"] = temperatura_valor
    simulacao.input["umidade"] = umidade_valor
    simulacao.input["vento"] = vento_valor

    simulacao.compute()

    if "risco" not in simulacao.output:
     valor = 50
    else:
      valor = simulacao.output["risco"]

# Ajuste para condições extremas de incêndio
    if temperatura_valor >= 40 and umidade_valor <= 20 and vento_valor >= 60:
        valor = max(valor, 90)


    if valor < 30:
        classificacao = "Baixo"
    elif valor < 60:
        classificacao = "Médio"
    elif valor < 85:
        classificacao = "Alto"
    else:
        classificacao = "Crítico"


    return {
        "risco": classificacao,
        "probabilidade": round(float(valor), 1),
        "justificativa": (
            f"Temperatura {temperatura_valor}°C, "
            f"umidade {umidade_valor}% e "
            f"vento {vento_valor} km/h "
            f"geraram risco {classificacao.lower()}."
        )
    }