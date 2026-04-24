"""
Práctica 10 – Estrategias para la construcción de algoritmos I
Módulo  : Algoritmo ávido (greedy) – Cambio de monedas

Instrucciones
    Implementa las funciones marcadas con TODO.
    Ejecuta el archivo directamente para verificar tu avance.
"""


# ---------------------------------------------------------------------------
# Problema A – Solución greedy
# ---------------------------------------------------------------------------

def cambio_greedy(monto: int, monedas: list) -> tuple | None:
    """
    Resuelve el problema de cambio con la estrategia ávida:
    en cada paso usa la moneda de mayor valor que quepa.
    """
    monedas_ordenadas = sorted(monedas, reverse=True)

    restante = monto
    usadas = []

    for moneda in monedas_ordenadas:
        cantidad = restante // moneda

        if cantidad > 0:
            usadas.extend([moneda] * cantidad)
            restante = restante % moneda

    if restante == 0:
        return usadas, len(usadas)
    else:
        return None


# ---------------------------------------------------------------------------
# Problema B – Solución óptima por programación dinámica
# ---------------------------------------------------------------------------

def cambio_optimo_dp(monto: int, monedas: list) -> tuple | None:
    """
    Resuelve el problema de cambio de manera óptima usando
    programación dinámica (número mínimo de monedas).
    """
    dp = [float("inf")] * (monto + 1)
    padre = [None] * (monto + 1)

    dp[0] = 0

    for i in range(1, monto + 1):
        for moneda in monedas:
            if moneda <= i:
                if dp[i - moneda] + 1 < dp[i]:
                    dp[i] = dp[i - moneda] + 1
                    padre[i] = moneda

    if dp[monto] == float("inf"):
        return None

    usadas = []
    actual = monto

    while actual > 0:
        moneda = padre[actual]

        if moneda is None:
            return None

        usadas.append(moneda)
        actual -= moneda

    return usadas, len(usadas)


# ---------------------------------------------------------------------------
# Problema C – Comparación: contraejemplos
# ---------------------------------------------------------------------------

def comparar_estrategias(monto_max: int, monedas: list) -> dict:
    """
    Para cada monto de 1 a monto_max, compara greedy vs DP.
    """
    montos_greedy_falla = []
    montos_greedy_suboptimo = []

    for monto in range(1, monto_max + 1):
        greedy = cambio_greedy(monto, monedas)
        dp = cambio_optimo_dp(monto, monedas)

        if greedy is None and dp is not None:
            montos_greedy_falla.append(monto)

        elif greedy is not None and dp is not None:
            total_greedy = greedy[1]
            total_dp = dp[1]

            if total_greedy > total_dp:
                montos_greedy_suboptimo.append(
                    (monto, total_greedy, total_dp)
                )

    return {
        "montos_greedy_falla": montos_greedy_falla,
        "montos_greedy_suboptimo": montos_greedy_suboptimo
    }


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Sistema canónico
    canonicas = [1, 2, 5, 10, 20, 50]
    print("=== Sistema canónico [1,2,5,10,20,50] ===")
    for monto in [11, 30, 63]:
        g = cambio_greedy(monto, canonicas)
        d = cambio_optimo_dp(monto, canonicas)
        print(f"  Monto {monto:>3}: greedy={g}  dp={d}")

    # Sistema no canónico – aquí greedy falla
    no_canonicas = [1, 3, 4]
    print("\n=== Sistema no canónico [1,3,4] ===")
    for monto in [6, 12, 15]:
        g = cambio_greedy(monto, no_canonicas)
        d = cambio_optimo_dp(monto, no_canonicas)
        print(f"  Monto {monto:>3}: greedy={g}  dp={d}")

    print("\n=== Análisis completo montos 1-60, sistema [1,3,4] ===")
    resultado = comparar_estrategias(60, no_canonicas)
    if resultado is not None:
        sub = resultado.get("montos_greedy_suboptimo", [])
        fal = resultado.get("montos_greedy_falla", [])
        print(f"  Casos subóptimos : {len(sub)}")
        print(f"  Casos con fallo  : {len(fal)}")
        if sub:
            print(f"  Primeros 5 subóptimos: {sub[:5]}")
    else:
        print("  comparar_estrategias aún no implementada")
