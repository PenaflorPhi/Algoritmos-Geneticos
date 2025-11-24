# -----------------------------------------------------------------------------
# Algoritmo Genético (AG) para la optimización de las dimensiones de una caja
#
# Problema:
#    Maximizar el volumen de una caja rectangular:
#
#        V(l, w, h) = l * w * h
#
#    Sujeto a las restricciones:
#        l \in [10.0, 50.0]   # largo  (cm)
#        w \in [10.0, 50.0]   # ancho  (cm)
#        h \in [ 5.0, 30.0]   # alto   (cm)
#
# Ángel Peñaflor, 2025
#
# Licencia: MIT
# -----------------------------------------------------------------------------
import random


# -----------------------------------------------------------------------------
# 1. Codificación binaria de las variables
#
# Cada variable (largo, ancho, alto) se representa mediante un cromosoma binario.
# Para este estudio usamos:
#
#    - 10 bits para l
#    - 10 bits para w
#    - 10 bits para h
#
# Lo que da un total de 30 bits por individuo.
# -----------------------------------------------------------------------------
def codificar(x: float, a: float, b: float, bits: int = 10) -> list[int]:
    if a >= b:
        raise ValueError("El límite inferior debe ser menor que el límite superior.")

    if x < a:
        x = a
    elif x > b:
        x = b

    max_int = (1 << bits) - 1

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
# 3. Generación de la población inicial
#
# La población inicial del algoritmo genético se construye generando
# cromosomas binarios de longitud fija.
#
# El tamaño del cromosoma depende del número de variables y los bits asignados
# a cada una. Para este caso:
#
#    - 10 bits por variable
#    - 3 variables (l, w, h)
# -----------------------------------------------------------------------------
def cromosoma_aleatorio(bits_por_var: int = 10, num_variables: int = 3) -> list[int]:
    total_bits = bits_por_var * num_variables
    return [random.randint(0, 1) for _ in range(total_bits)]


def poblacion_inicial(
    tamano: int,
    bits_por_var: int = 10,
    num_variables: int = 3,
) -> list[list[int]]:
    return [cromosoma_aleatorio(bits_por_var, num_variables) for _ in range(tamano)]


# -----------------------------------------------------------------------------
# 4. Decodificación del cromosoma y función de aptitud
#
# Cada cromosoma binario representa las tres variables del problema:
#
#    - length: largo de la caja
#    - width: ancho de la caja
#    - height: alto  de la caja

# La aptitud de un individuo será el volumen de la caja:
#
#        V(l, w, h) = l * w * h
# -----------------------------------------------------------------------------
L_MIN, L_MAX = 10.0, 50.0
W_MIN, W_MAX = 10.0, 50.0
H_MIN, H_MAX = 5.0, 30.0

RANGOS = [
    (L_MIN, L_MAX),  # rango para l
    (W_MIN, W_MAX),  # rango para w
    (H_MIN, H_MAX),  # rango para h
]


def decodificar_individuo(
    cromosoma: list[int],
    rangos: list[tuple[float, float]] = RANGOS,
    bits_por_var: int = 10,
) -> tuple[float, float, float]:
    """
    Convierte un cromosoma binario completo en las tres variables reales (l, w, h).

    Parámetros:
        cromosoma  : lista de bits que representa al individuo
        rangos     : lista de tuplas (a, b) con el rango de cada variable
        bits_por_var : número de bits asignados a cada variable

    Devuelve:
        Una tupla (l, w, h) con las dimensiones decodificadas.
    """
    num_vars = len(rangos)
    esperado = num_vars * bits_por_var

    if len(cromosoma) != esperado:
        raise ValueError(
            f"La longitud del cromosoma ({len(cromosoma)}) no coincide con "
            f"num_vars * bits_por_var = {esperado}."
        )

    valores: list[float] = []
    for i, (a, b) in enumerate(rangos):
        inicio = i * bits_por_var
        fin = (i + 1) * bits_por_var
        sub_bits = cromosoma[inicio:fin]
        x = decodificar(sub_bits, a, b)
        valores.append(x)

    length, width, height = valores
    return length, width, height


def volumen_caja(length: float, width: float, height: float) -> float:
    return length * width * height


def aptitud(cromosoma: list[int]) -> float:
    length, width, height = decodificar_individuo(cromosoma)
    return volumen_caja(length, width, height)


def evaluar_poblacion(poblacion: list[list[int]]) -> list[float]:
    return [aptitud(individuo) for individuo in poblacion]


# -----------------------------------------------------------------------------
# 5. Cálculo de probabilidades de selección
#
# A partir de las aptitudes de la población, calculamos la probabilidad de
# selección de cada individuo. Usaremos selección proporcional a la aptitud:
#
#      p_i = f_i / sum_j f_j
#
# donde:
#      f_i  = aptitud del individuo i
#      p_i  = probabilidad de selección del individuo i
# -----------------------------------------------------------------------------
def probabilidades_seleccion(aptitudes: list[float]) -> list[float]:
    if not aptitudes:
        raise ValueError("La lista de aptitudes no puede estar vacía.")

    total_aptitud = sum(aptitudes)

    if total_aptitud <= 0.0:
        n = len(aptitudes)
        return [1.0 / n] * n

    return [f_i / total_aptitud for f_i in aptitudes]


def resumen_poblacion(poblacion: list[list[int]]) -> None:
    valores_aptitud = evaluar_poblacion(poblacion)
    probs = probabilidades_seleccion(valores_aptitud)

    print("Idx |        l     w     h |   Aptitud (volumen)  |  Prob. selección")
    print("----+----------------------+----------------------+------------------")
    for i, (ind, fit, p) in enumerate(zip(poblacion, valores_aptitud, probs)):
        length, width, height = decodificar_individuo(ind)
        print(
            f"{i:3d} | {length:7.2f} {width:7.2f} {height:7.2f} | {fit:20.2f} | {p:16.4f}"
        )


# -----------------------------------------------------------------------------
# 6. Selección de los dos individuos con mayor probabilidad
#
# A partir de las probabilidades de selección p_i, elegimos a los dos
# individuos con mayor probabilidad (según el enunciado).
# -----------------------------------------------------------------------------
def indices_mejores(probabilidades: list[float], k: int = 2) -> list[int]:
    """
    Devuelve los índices de los k individuos con mayor probabilidad.

    Parámetros:
        probabilidades : lista de probabilidades p_i (una por individuo)
        k              : número de individuos a seleccionar (por defecto 2)

    Devuelve:
        Lista con los k mejores individuos, ordenados de
        mayor a menor probabilidad.
    """
    if k <= 0:
        raise ValueError("k debe ser un entero positivo.")
    if k > len(probabilidades):
        raise ValueError("k no puede ser mayor que el tamaño de la población.")

    orden = sorted(
        range(len(probabilidades)),
        key=lambda i: probabilidades[i],
        reverse=True,
    )
    return orden[:k]


def seleccionar_mejores(
    poblacion: list[list[int]],
    probabilidades: list[float],
    k: int = 2,
) -> list[list[int]]:
    """
    Selecciona los k mejores individuos de la población según sus probabilidades.
    """
    idx = indices_mejores(probabilidades, k)
    return [poblacion[i] for i in idx]


# -----------------------------------------------------------------------------
# 7. Operador de cruce de un punto
#
# Dado un par de padres (cromosomas binarios de igual longitud), elegimos
# un punto de cruce y generamos dos hijos intercambiando los segmentos.
# -----------------------------------------------------------------------------
def cruce_un_punto(padre1: list[int], padre2: list[int]) -> tuple[list[int], list[int]]:
    if len(padre1) != len(padre2):
        raise ValueError("Ambos padres deben tener la misma longitud.")
    n_bits = len(padre1)

    if n_bits < 2:
        return padre1[:], padre2[:]

    punto = random.randint(1, n_bits - 1)

    hijo1 = padre1[:punto] + padre2[punto:]
    hijo2 = padre2[:punto] + padre1[punto:]

    return hijo1, hijo2


# -----------------------------------------------------------------------------
# 8. Operador de mutación
#
# La mutación se realiza recorriendo cada bit del cromosoma y, con una
# probabilidad p_mut, se invierte el bit:
#
#    0 -> 1
#    1 -> 0
# -----------------------------------------------------------------------------
def mutar_cromosoma(cromosoma: list[int], p_mut: float) -> list[int]:
    if not (0.0 <= p_mut <= 1.0):
        raise ValueError("p_mut debe estar en el intervalo [0, 1].")

    nuevo = []
    for bit in cromosoma:
        if random.random() < p_mut:
            nuevo.append(1 - bit)  # Invierte el bit
        else:
            nuevo.append(bit)
    return nuevo


def generar_hijos_desde_mejores(
    poblacion: list[list[int]], p_mut: float = 0.01
) -> tuple[list[int], list[int]]:
    aptitudes = evaluar_poblacion(poblacion)
    probs = probabilidades_seleccion(aptitudes)
    mejores = seleccionar_mejores(poblacion, probs, k=2)
    padre1, padre2 = mejores

    hijo1, hijo2 = cruce_un_punto(padre1, padre2)

    hijo1_mut = mutar_cromosoma(hijo1, p_mut)
    hijo2_mut = mutar_cromosoma(hijo2, p_mut)

    return hijo1_mut, hijo2_mut


# -----------------------------------------------------------------------------
# 9. Bucle evolutivo del Algoritmo Genético
#
# En cada generación se realiza:
#   1) Evaluación de la población
#   2) Cálculo de probabilidades de selección
#   3) Selección de los dos mejores individuos
#   4) Cruce de un punto
#   5) Mutación de los hijos
#   6) Reemplazo de los dos peores individuos de la población
# -----------------------------------------------------------------------------


def evolucionar(
    poblacion: list[list[int]],
    generaciones: int = 50,
    p_mut: float = 0.01,
) -> list[list[int]]:
    """
    Ejecuta el ciclo evolutivo completo del algoritmo genético.

    Parámetros:
        poblacion    : población inicial
        generaciones : número de iteraciones
        p_mut        : probabilidad de mutación por bit

    Devuelve:
        La población final después de 'generaciones' iteraciones.
    """
    for gen in range(generaciones):
        aptitudes = evaluar_poblacion(poblacion)
        probs = probabilidades_seleccion(aptitudes)

        # Selección de los dos mejores padres
        mejores = seleccionar_mejores(poblacion, probs, k=2)
        padre1, padre2 = mejores

        # Cruce y mutación
        hijo1, hijo2 = cruce_un_punto(padre1, padre2)
        hijo1 = mutar_cromosoma(hijo1, p_mut)
        hijo2 = mutar_cromosoma(hijo2, p_mut)

        # Identificamos los dos peores individuos
        peores = sorted(range(len(aptitudes)), key=lambda i: aptitudes[i])[:2]

        # Reemplazamos los dos peores por los hijos generados
        poblacion[peores[0]] = hijo1
        poblacion[peores[1]] = hijo2

        # (Opcional) imprimir progreso
        # print(f"Generación {gen+1}: mejor aptitud = {max(aptitudes):.2f}")

    return poblacion


def main():
    seed = random.randint(0, 10000)
    print(f"Semilla aleatoria: {seed}")
    random.seed(seed)

    # 1) Creamos la población inicial
    pobl = poblacion_inicial(tamano=100)

    print("\nPoblación inicial:")
    resumen_poblacion(pobl)

    # 2) Ejecutamos el AG durante 50 generaciones
    pobl_final = evolucionar(pobl, generaciones=50, p_mut=0.05)

    # 3) Evaluamos la población final
    print("\nPoblación final después de 50 generaciones:")
    resumen_poblacion(pobl_final)

    # 4) Obtenemos el mejor individuo final
    aptitudes_finales = evaluar_poblacion(pobl_final)
    mejor_indice = max(
        range(len(aptitudes_finales)), key=lambda i: aptitudes_finales[i]
    )
    mejor = pobl_final[mejor_indice]

    l, w, h = decodificar_individuo(mejor)
    fit = volumen_caja(l, w, h)

    print("\nMejor individuo encontrado:")
    print(f"  l = {l:.2f} cm, w = {w:.2f} cm, h = {h:.2f} cm")
    print(f"  Volumen = {fit:.2f} cm^3")
    print(f"  Cromosoma: {mejor}")


if __name__ == "__main__":
    main()
