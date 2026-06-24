"""
Bateria de testes do motor fuzzy.
Execucao: python tests/test_engine.py  (a partir da raiz do projeto)
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from components.fuzzy_engine import calcular_risco

VERDE    = "\033[92m"
VERMELHO = "\033[91m"
CINZA    = "\033[90m"
RESET    = "\033[0m"

# ---------------------------------------------------------------------------
# Cenarios com classificacao esperada
# (descricao, temperatura C, umidade %, vento km/h, classificacao esperada)
# ---------------------------------------------------------------------------
CENARIOS = [
    # Baixo
    ("Dia frio e umido",             10, 85, 10, "Baixo"),
    ("Inverno tipico",                5, 90,  5, "Baixo"),
    ("Primavera amena",              15, 75, 15, "Baixo"),

    # Medio
    ("Tarde de primavera seca",      28, 30, 25, "Médio"),
    ("Frio com vento forte",         10, 15, 70, "Médio"),
    ("Temperatura moderada",         25, 50, 20, "Médio"),
    ("Calor extremo + chuva",        48, 85, 20, "Médio"),

    # Alto
    ("Verao quente e seco",          38, 20, 30, "Alto"),
    ("35C + umidade critica",        35,  0, 20, "Alto"),
    ("40C + umidade baixa",          40, 25, 20, "Alto"),
    ("Temp critica + seco + fraco",  48, 25, 20, "Alto"),

    # Critico
    ("Onda de calor extrema",        48,  5, 90, "Crítico"),
    ("Condicao maxima",              50,  0, 100, "Crítico"),
    ("Temp critica + vento critico", 48, 10, 85, "Crítico"),
    # Caso de borda: 45C gera 84.x% (Alto, perto do limiar de 85%)
    ("Borda: 45C + 5% + 90km",      45,  5, 90, "Alto"),

    # Regressoes (bugs corrigidos)
    ("Regr: frio+seco+vento != Critico",   5, 10, 88, "Médio"),
    ("Regr: 35C+0%+20km deve ser Alto",   35,  0, 20, "Alto"),
]

# ---------------------------------------------------------------------------
# Teste de monotonicidade
# Vento crescente NAO pode reduzir o risco (era o bug do paradoxo do vento)
# ---------------------------------------------------------------------------
ORDEM = {"Baixo": 0, "Médio": 1, "Alto": 2, "Crítico": 3}

MONOTONICOS = [
    ("35C + 0% umidade",   35,  0, [20, 40, 80, 100]),
    ("40C + 10% umidade",  40, 10, [10, 30, 70,  95]),
    ("30C + 5% umidade",   30,  5, [ 0, 25, 60,  90]),
]

# ---------------------------------------------------------------------------

def sep(n=62):
    print("  " + "=" * n)


def run():
    passou = 0
    falhou = 0

    print()
    sep()
    print("  TESTES DO MOTOR FUZZY -- classificacao esperada")
    sep()

    for desc, t, u, v, esperado in CENARIOS:
        r    = calcular_risco(t, u, v)
        real = r["risco"]
        prob = r["probabilidade"]
        ok   = real == esperado

        entradas = f"temp={t}C  umid={u}%  vento={v}km/h"

        if ok:
            print(f"  {VERDE}PASS{RESET}  {desc}")
            print(f"       Entrada : {CINZA}{entradas}{RESET}")
            print(f"       Saida   : {CINZA}{real} ({prob}%){RESET}")
            passou += 1
        else:
            print(f"  {VERMELHO}FAIL{RESET}  {desc}")
            print(f"       Entrada : {entradas}")
            print(f"       Esperado: {VERMELHO}{esperado}{RESET}  |  "
                  f"Obtido: {VERMELHO}{real} ({prob}%){RESET}")
            falhou += 1

    print()
    sep()
    print("  MONOTONICIDADE -- vento crescente nao pode reduzir o risco")
    sep()

    for desc, t, u, ventos in MONOTONICOS:
        resultados = [(v, calcular_risco(t, u, v)) for v in ventos]
        ok = all(
            ORDEM[resultados[i + 1][1]["risco"]] >= ORDEM[resultados[i][1]["risco"]]
            for i in range(len(resultados) - 1)
        )
        progresso = "  ->  ".join(
            f"{v}km/h => {r['risco']} ({r['probabilidade']}%)"
            for v, r in resultados
        )
        if ok:
            print(f"  {VERDE}PASS{RESET}  {desc}  [temp={t}C  umid={u}%]")
            print(f"       {CINZA}{progresso}{RESET}")
            passou += 1
        else:
            print(f"  {VERMELHO}FAIL{RESET}  {desc}  [temp={t}C  umid={u}%]")
            print(f"       {VERMELHO}{progresso}{RESET}  <- risco caiu com vento maior")
            falhou += 1

    print()
    sep()
    total = passou + falhou
    cor   = VERDE if falhou == 0 else VERMELHO
    print(f"  {cor}Resultado: {passou}/{total} passaram{RESET}")
    sep()
    print()

    return falhou == 0


if __name__ == "__main__":
    ok = run()
    sys.exit(0 if ok else 1)
