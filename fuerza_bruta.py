"""
Práctica 10 – Estrategias para la construcción de algoritmos I
Módulo  : Fuerza bruta

Instrucciones
    Implementa las funciones marcadas con TODO.
    Ejecuta el archivo directamente para verificar tu avance.
"""

import itertools
import string
import time

# ---------------------------------------------------------------------------
# Alfabetos predefinidos
# ---------------------------------------------------------------------------
DIGITOS    = string.digits                      # '0123456789'
MINUSCULAS = string.ascii_lowercase             # 'abcdefghijklmnopqrstuvwxyz'
ALNUM      = string.ascii_letters + string.digits


# ---------------------------------------------------------------------------
# Problema A – Generación y búsqueda exhaustiva
# ---------------------------------------------------------------------------

import itertools
import string
import time

# ---------------------------------------------------------------------------
# Alfabetos predefinidos
# ---------------------------------------------------------------------------
DIGITOS    = string.digits                  # '0123456789'
MINUSCULAS = string.ascii_lowercase         # 'abcdefghijklmnopqrstuvwxyz'
ALNUM      = string.ascii_letters + string.digits

# ---------------------------------------------------------------------------
# Problema A – Generación y búsqueda exhaustiva
# ---------------------------------------------------------------------------

def generar_candidatos(alfabeto: str, longitud: int):
    """
    Genera (como iterador) todas las cadenas de exactamente 'longitud'
    caracteres del alfabeto dado.
    """
    # Generamos el producto cartesiano y unimos cada tupla en una cadena
    for tupla in itertools.product(alfabeto, repeat=longitud):
        yield "".join(tupla)

def buscar_cadena_objetivo(objetivo: str, alfabeto: str, 
                           min_len: int = 1) -> tuple:
    """
    Busca 'objetivo' recorriendo todas las cadenas del alfabeto de longitud
    min_len hasta len(objetivo) (inclusive).
    """
    intentos = 0
    inicio   = time.perf_counter()

    for longitud in range(min_len, len(objetivo) + 1):
        for candidato in generar_candidatos(alfabeto, longitud):
            intentos += 1
            if candidato == objetivo:
                tiempo = time.perf_counter() - inicio
                return (True, intentos, tiempo)

    tiempo = time.perf_counter() - inicio
    return (False, intentos, tiempo)


# ---------------------------------------------------------------------------
# Problema B – Análisis de crecimiento
# ---------------------------------------------------------------------------

def combinar_teoricas(alfabeto: str, min_len: int, max_len: int) -> int:
    """
    Calcula el número teórico de cadenas a explorar.
    Fórmula: suma de |alfabeto|^k para k en [min_len, max_len]
    """
    base = len(alfabeto)
    return sum(base**k for k in range(min_len, max_len + 1))


# ---------------------------------------------------------------------------
# Problema C – Optimización con poda por prefijo
# ---------------------------------------------------------------------------


def buscar_con_poda(objetivo: str, alfabeto: str, 
                    prefijos_validos: set) -> tuple:
    """
    Variante con poda: verifica que cada prefijo propio esté en 'prefijos_validos'.
    """
    intentos = 0
    inicio   = time.perf_counter()

    for longitud in range(1, len(objetivo) + 1):
        for partes in itertools.product(alfabeto, repeat=longitud):
            candidato = "".join(partes)
            
            # PODA: Verificar prefijos propios (de longitud 1 hasta longitud-1)
            # Si el prefijo no es válido, no tiene sentido seguir explorando esta rama.
            poda_activa = False
            for k in range(1, len(candidato)):
                if candidato[:k] not in prefijos_validos:
                    poda_activa = True
                    break
            
            if poda_activa:
                continue

            intentos += 1
            if candidato == objetivo:
                tiempo = time.perf_counter() - inicio
                return (True, intentos, tiempo)

    tiempo = time.perf_counter() - inicio
    return (False, intentos, tiempo)

# ---------------------------------------------------------------------------
if __name__ == "__main__":
    objetivo = "az"
    print("=== Búsqueda por fuerza bruta ===")
    encontrada, intentos, t = buscar_cadena_objetivo(objetivo, MINUSCULAS)
    if encontrada:
        print(f"  Objetivo : '{objetivo}'")
        print(f"  Intentos : {intentos}")
        print(f"  Tiempo   : {t:.4f} s")
        print(f"  Tasa     : {intentos / t:.0f} candidatos/s")
    
    print("\n=== Combinaciones teóricas ===")
    for max_len in [3, 4, 5]:
        n = combinar_teoricas(DIGITOS, 1, max_len)
        print(f"  Dígitos hasta longitud {max_len}: {n:,} candidatos")
