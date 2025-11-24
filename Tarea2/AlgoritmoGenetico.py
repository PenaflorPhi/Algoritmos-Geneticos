# -----------------------------------------------------------------------------
# Algoritmo Genético (AG) para la optimización de una función de dos variables
#
# Problema:
#    Minimizar la función:
#
#        f(x, y) = 20 + x^2 + y^2 - cos(2\pi x) + cos(2\pi y)
#
#    Sujeto a las restricciones:
#        x \in [-5.12, 5.12]
#        y \in [-5.12, 5.12]
#
# Ángel Peñaflor, 2025
#
# Licencia: MIT
# -----------------------------------------------------------------------------
import csv
import math
import random


# -----------------------------------------------------------------------------
# 1. Codificación binaria de las variables
#
# Cada variable (x, y) se representa mediante un cromosoma binario de longitud fija.
# En este caso:
#
#    - 10 bits para x
#    - 10 bits para y
# -----------------------------------------------------------------------------
def codificar(x: float, a: float, b: float, bits: int = 10) -> list[int]:
    if a >= b:
        raise ValueError("El límite inferior debe ser menor que el límite superior.")

    if x < a:
        x = a
    elif x > b:
        x = b

    max_int = (1 << bits) - 1

    # Escalamos x al entero k en [0, max_int]
    k = round((x - a) / (b - a) * max_int)
    k = max(0, min(max_int, k))

    n_bits = [(k >> i) & 1 for i in range(bits - 1, -1, -1)]
    return n_bits


def decodificar(bits: list[int], a: float, b: float) -> float:
    if a >= b:
        raise ValueError("El límite inferior debe ser menor que el límite superior.")

    n_bits = len(bits)
    max_int = (1 << n_bits) - 1

    k = 0
    for bit in bits:
        k = (k << 1) | (bit & 1)

    x = a + (k / max_int) * (b - a)
    return x


# -----------------------------------------------------------------------------
# 2. Definición de la función de aptitud
#
# La función de aptitud se define como el negativo de la función objetivo:
#
#        aptitud(x, y) = -f(x, y)
#
# -----------------------------------------------------------------------------
def f_objetivo(x: float, y: float) -> float:
    return 20 + x**2 + y**2 - math.cos(2 * math.pi * x) + math.cos(2 * math.pi * y)


def aptitud(x: float, y: float) -> float:
    return -f_objetivo(x, y)


# -----------------------------------------------------------------------------
# 3. Generación de la población inicial
#
# La población inicial del algoritmo genético se construye generando
# cromosomas binarios.
# Cada cromosoma corresponde a un individuo y está compuesto por 20 bits:
#    - 10 bits asignados a la variable x
#    - 10 bits asignados a la variable y
# -----------------------------------------------------------------------------
def cromosoma_aleatorio(n_bits: int = 10) -> list[int]:
    return [random.randint(0, 1) for _ in range(2 * n_bits)]


def poblacion_inicial(tamano: int, n_bits: int = 10) -> list[list[int]]:
    return [cromosoma_aleatorio(n_bits) for _ in range(tamano)]


# -----------------------------------------------------------------------------
# 4. Operadores genéticos: selección, cruce y mutación
#
# En esta etapa se implementan los operadores básicos del algoritmo genético
# que permiten la evolución de la población a lo largo de las generaciones:
#
#    - Selección:
#         Se eligen individuos de la población en función de su aptitud,
#         privilegiando aquellos con mejores valores de aptitud para que
#         contribuyan más frecuentemente al siguiente conjunto de soluciones.
#
#    - Cruce:
#         A partir de pares de individuos seleccionados (padres), se combinan
#         sus cromosomas para generar nuevos individuos (hijos). En este
#         problema se emplea un cruce de un punto sobre cromosomas binarios.
#
#    - Mutación:
#         Se altera aleatoriamente el valor de algunos bits en los cromosomas,
#         con una baja probabilidad. Este operador introduce variación
#         genética adicional y ayuda a evitar la convergencia prematura hacia
#         óptimos locales.
# -----------------------------------------------------------------------------
def evaluar_poblacion(
    poblacion: list[list[int]],
    a_x: float,
    b_x: float,
    a_y: float,
    b_y: float,
    n_bits: int = 10,
) -> list[float]:
    aptitudes = []
    for individuo in poblacion:
        bits_x = individuo[:n_bits]
        bits_y = individuo[n_bits : 2 * n_bits]
        x = decodificar(bits_x, a_x, b_x)
        y = decodificar(bits_y, a_y, b_y)
        aptitudes.append(aptitud(x, y))
    return aptitudes


def seleccion_torneo(
    poblacion: list[list[int]],
    aptitudes: list[float],
    tamano_torneo: int = 3,
) -> list[list[int]]:
    nueva_poblacion = []
    n = len(poblacion)
    for _ in range(n):
        indices = [random.randint(0, n - 1) for _ in range(tamano_torneo)]
        mejor_indice = max(indices, key=lambda i: aptitudes[i])
        nueva_poblacion.append(poblacion[mejor_indice][:])
    return nueva_poblacion


def cruce_un_punto(
    padre1: list[int],
    padre2: list[int],
    probabilidad_cruce: float = 0.7,
) -> tuple[list[int], list[int]]:
    if len(padre1) != len(padre2):
        raise ValueError("Los padres deben tener la misma longitud.")

    n = len(padre1)

    if random.random() >= probabilidad_cruce:
        return padre1, padre2

    punto_cruce = random.randint(1, n - 1)
    hijo1 = padre1[:punto_cruce] + padre2[punto_cruce:]
    hijo2 = padre2[:punto_cruce] + padre1[punto_cruce:]

    return hijo1, hijo2


def aplicar_cruce_poblacion(
    poblacion: list[list[int]],
    probabilidad_cruce: float = 0.7,
) -> list[list[int]]:
    nueva: list[list[int]] = []
    n = len(poblacion)

    for i in range(0, n - 1, 2):
        padre1 = poblacion[i]
        padre2 = poblacion[i + 1]
        hijo1, hijo2 = cruce_un_punto(padre1, padre2, probabilidad_cruce)
        nueva.extend([hijo1, hijo2])

    if n % 2 == 1:
        nueva.append(poblacion[-1][:])

    return nueva


def mutar_cromosoma(
    cromosoma: list[int], probabilidad_mutacion: float = 0.01
) -> list[int]:
    nuevo_cromosoma: list[int] = []
    for bit in cromosoma:
        if random.random() < probabilidad_mutacion:
            nuevo_cromosoma.append(1 - bit)  # flip
        else:
            nuevo_cromosoma.append(bit)
    return nuevo_cromosoma


def aplicar_mutacion_poblacion(
    poblacion: list[list[int]],
    probabilidad_mutacion: float = 0.01,
) -> list[list[int]]:
    return [mutar_cromosoma(ind, probabilidad_mutacion) for ind in poblacion]


# -----------------------------------------------------------------------------
# 8. Bucle principal del algoritmo genético
#
# En este bloque se orquesta el flujo completo del algoritmo genético:
#
#    1) Inicialización:
#           - Se genera una población inicial de cromosomas binarios aleatorios.
#
#    2) Evaluación:
#           - En cada generación se calcula la aptitud de todos los individuos
#             de la población a partir de la función objetivo.
#
#    3) Aplicación de operadores genéticos:
#           - Selección: se eligen individuos con mejor desempeño para reproducirse.
#           - Cruce: se combinan cromosomas de pares de padres para producir hijos.
#           - Mutación: se modifican aleatoriamente bits de los cromosomas con
#             baja probabilidad, manteniendo la diversidad genética.
#
#    4) Iteración:
#           - Los pasos de evaluación y aplicación de operadores se repiten
#             durante un número fijo de generaciones, permitiendo que la
#             población evolucione hacia soluciones con mejor aptitud.
#
# Al finalizar el bucle, se selecciona el mejor individuo encontrado y se
# reporta su ubicación en el espacio (x, y) junto con el valor de f(x, y).
# -----------------------------------------------------------------------------


def algoritmo_genetico(
    generaciones: int = 100,
    tamano_poblacion: int = 30,
    n_bits: int = 10,
    a_x: float = -5.12,
    b_x: float = 5.12,
    a_y: float = -5.12,
    b_y: float = 5.12,
    probabilidad_cruce: float = 0.7,
    probabilidad_mutacion: float = 0.01,
    ruta_csv: str | None = "algoritmo_genetico_historial.csv",
) -> tuple[list[int], float, float, float]:
    """
    Ejecuta un algoritmo genético (AG) para minimizar la función objetivo
    f(x, y) = 20 + x^2 + y^2 - cos(2πx) + cos(2πy), donde las variables x e y
    están acotadas dentro del intervalo [-5.12, 5.12].

    El AG utiliza una representación binaria mediante cromosomas de 2*n_bits bits:
    n_bits para x y n_bits para y. La minimización se implementa definiendo
    la aptitud como el negativo de la función objetivo, de modo que el
    algoritmo opera bajo un esquema de maximización tradicional.

    Parámetros:
        generaciones (int):
            Número total de generaciones a ejecutar.
        tamano_poblacion (int):
            Cantidad de individuos en la población.
        n_bits (int):
            Número de bits asignados a cada variable del cromosoma.
        a_x, b_x (float):
            Límites inferior y superior para la variable x.
        a_y, b_y (float):
            Límites inferior y superior para la variable y.
        probabilidad_cruce (float):
            Probabilidad de que ocurra el cruce entre dos padres.
        probabilidad_mutacion (float):
            Probabilidad de mutar cada bit del cromosoma.
        ruta_csv (str | None):
            Ruta del archivo CSV donde se registrará la evolución del AG.
            Si es None, no se guarda archivo.

    Retorna:
        (mejor_cromosoma, mejor_x, mejor_y, mejor_f):
            - mejor_cromosoma (list[int]): Cromosoma binario del mejor individuo.
            - mejor_x (float): Valor de x decodificado a partir del cromosoma.
            - mejor_y (float): Valor de y decodificado a partir del cromosoma.
            - mejor_f (float): Valor mínimo aproximado de la función objetivo.
    """
    poblacion = poblacion_inicial(tamano_poblacion, n_bits)

    historial: list[dict] = []

    for gen in range(generaciones):
        # Evaluación
        aptitudes = evaluar_poblacion(poblacion, a_x, b_x, a_y, b_y, n_bits)

        # Métricas de la generación
        mejor_aptitud = max(aptitudes)
        promedio_aptitud = sum(aptitudes) / len(aptitudes)
        idx_mejor = max(range(len(poblacion)), key=lambda i: aptitudes[i])
        crom_mejor_gen = poblacion[idx_mejor]

        bits_x_gen = crom_mejor_gen[:n_bits]
        bits_y_gen = crom_mejor_gen[n_bits : 2 * n_bits]
        x_gen = decodificar(bits_x_gen, a_x, b_x)
        y_gen = decodificar(bits_y_gen, a_y, b_y)
        f_gen = f_objetivo(x_gen, y_gen)

        # Registro (para CSV / gráficas)
        historial.append(
            {
                "generacion": gen + 1,
                "mejor_aptitud": mejor_aptitud,
                "aptitud_promedio": promedio_aptitud,
                "mejor_x": x_gen,
                "mejor_y": y_gen,
                "f_mejor": f_gen,
            }
        )

        # (Opcional) imprimir en consola
        print(
            f"Generación {gen + 1:3d}: "
            f"Mejor aptitud = {mejor_aptitud:.6f}, "
            f"Aptitud promedio = {promedio_aptitud:.6f}"
        )

        # Selección, cruce y mutación
        poblacion = seleccion_torneo(poblacion, aptitudes, tamano_torneo=3)
        poblacion = aplicar_cruce_poblacion(poblacion, probabilidad_cruce)
        poblacion = aplicar_mutacion_poblacion(poblacion, probabilidad_mutacion)

    # Evaluación final
    aptitudes_finales = evaluar_poblacion(poblacion, a_x, b_x, a_y, b_y, n_bits)
    mejor_indice = max(range(len(poblacion)), key=lambda i: aptitudes_finales[i])
    mejor_cromosoma = poblacion[mejor_indice]

    bits_x = mejor_cromosoma[:n_bits]
    bits_y = mejor_cromosoma[n_bits : 2 * n_bits]
    mejor_x = decodificar(bits_x, a_x, b_x)
    mejor_y = decodificar(bits_y, a_y, b_y)
    mejor_f = f_objetivo(mejor_x, mejor_y)

    # Guardar CSV si se solicitó
    if ruta_csv is not None:
        with open(ruta_csv, mode="w", newline="", encoding="utf-8") as f:
            escritor = csv.DictWriter(
                f,
                fieldnames=[
                    "generacion",
                    "mejor_aptitud",
                    "aptitud_promedio",
                    "mejor_x",
                    "mejor_y",
                    "f_mejor",
                ],
            )
            escritor.writeheader()
            escritor.writerows(historial)

    return mejor_cromosoma, mejor_x, mejor_y, mejor_f


def main():
    mejor_crom, x_opt, y_opt, f_opt = algoritmo_genetico()

    print("-------------------------------------------------------------")
    print("RESULTADOS DEL ALGORITMO GENÉTICO")
    print("-------------------------------------------------------------")
    print("El algoritmo localizó el mínimo aproximado de la función en:")
    print(f"   x* = {x_opt:.6f}")
    print(f"   y* = {y_opt:.6f}")
    print()
    print(f"Valor mínimo encontrado de f(x, y): {f_opt:.6f}")
    print()
    print("Cromosoma binario asociado al mínimo:")
    print(mejor_crom)
    print("-------------------------------------------------------------")


if __name__ == "__main__":
    main()
