# -----------------------------------------------------------------------------
# Mutación en espacio real para una barra nutricional
#
# Contexto:
#   Este módulo implementa operadores básicos sobre individuos representados
#   en espacio real (listas de flotantes), en el contexto de una mezcla de
#   ingredientes para una barra nutricional.
#
#   Cada individuo está formado por 4 genes, que representan gramos de:
#       0) Proteína de suero
#       1) Avena
#       2) Mantequilla de almendra
#       3) Azúcar
#
#   Cada gen está acotado por un intervalo [mínimo, máximo] específico.
#
#   El objetivo principal de este archivo es:
#       - Generar individuos y poblaciones iniciales en espacio real.
#       - Aplicar un operador de mutación gaussiana respetando límites.
#       - Mostrar cómo cambian los individuos a lo largo de varias generaciones.
#
# Autor:  Ángel Peñaflor, 2025
# Licencia: MIT
# -----------------------------------------------------------------------------
import random

# -----------------------------------------------------------------------------
# 1. Límites de las variables (genes)
#
# Cada tupla en LIMITES representa el intervalo permitido de gramos para
# cada ingrediente de la barra nutricional:
#
#   LIMITES[i] = (minimo_i, maximo_i)
#
# El orden de los ingredientes es:
#   0: proteína de suero
#   1: avena
#   2: mantequilla de almendra
#   3: azúcar
# -----------------------------------------------------------------------------
LIMITES = [
    (10.0, 50.0),  # proteína de suero
    (20.0, 100.0),  # avena
    (5.0, 30.0),  # mantequilla de almendra
    (0.0, 20.0),  # azúcar
]


# -----------------------------------------------------------------------------
# 2. Generación de individuos y población inicial (representación real)
#
# En este módulo los individuos se representan como listas de números reales
# (float), donde cada posición corresponde a la cantidad (en gramos) de un
# ingrediente específico.
#
#   individuo = [suero, avena, mantequilla_almendra, azucar]
#
# La función `individuo_aleatorio` genera un solo individuo muestreando
# uniformemente dentro de los límites de cada ingrediente.
#
# La función `poblacion_inicial_real` construye una lista de individuos
# independientes, que servirá como población inicial para un algoritmo genético
# basado en variables reales.
# -----------------------------------------------------------------------------
def individuo_aleatorio() -> list[float]:
    """
    Genera un individuo aleatorio respetando los límites de cada ingrediente.

    Retorna:
        list[float]: Lista con 4 valores en gramos, en el siguiente orden:
            [proteína de suero, avena, mantequilla de almendra, azúcar]
    """
    return [
        random.uniform(10, 50),  # proteína de suero
        random.uniform(20, 100),  # avena
        random.uniform(5, 30),  # mantequilla de almendra
        random.uniform(0, 20),  # azúcar
    ]


def poblacion_inicial_real(tamano: int) -> list[list[float]]:
    """
    Genera una población inicial de individuos en espacio real.

    Parámetros:
        tamano (int):
            Número de individuos a generar.

    Retorna:
        list[list[float]]: Lista de individuos. Cada individuo es una lista de
        4 valores flotantes que representan gramos de los ingredientes.
    """
    return [individuo_aleatorio() for _ in range(tamano)]


# -----------------------------------------------------------------------------
# 3. Función auxiliar de recorte
#
# La función `recortar` garantiza que un valor permanezca dentro de un
# intervalo [minimo, maximo]. Se utiliza después de aplicar la mutación
# gaussiana para asegurar que los genes sigan siendo válidos.
# -----------------------------------------------------------------------------
def recortar(valor: float, minimo: float, maximo: float) -> float:
    """
    Recorta un valor para que permanezca dentro del intervalo [minimo, maximo].

    Parámetros:
        valor (float):
            Valor original.
        minimo (float):
            Límite inferior permitido.
        maximo (float):
            Límite superior permitido.

    Retorna:
        float: Valor ajustado para estar dentro del intervalo.
    """
    return max(minimo, min(maximo, valor))


# -----------------------------------------------------------------------------
# 4. Operador de mutación gaussiana para individuos reales
#
# La función `mutar_individuo_real` implementa un operador de mutación
# en espacio real. Para cada gen del individuo:
#
#   - Con probabilidad `probabilidad_mutacion` se le suma una perturbación
#     gaussiana N(0, sigma).
#   - Posteriormente, el valor resultante se recorta al intervalo permitido
#     para ese gen usando `LIMITES`.
#
# Si la mutación no se aplica (según la probabilidad), el valor original
# del gen se copia sin cambios.
#
# Nota: La función retorna un nuevo individuo, no modifica el original in-place.
# -----------------------------------------------------------------------------
def mutar_individuo_real(
    individuo: list[float],
    probabilidad_mutacion: float = 0.1,
    sigma: float = 1.0,
) -> list[float]:
    """
    Aplica mutación gaussiana a un individuo representado en espacio real.

    Parámetros:
        individuo (list[float]):
            Individuo original, una lista de valores reales (gramos).
        probabilidad_mutacion (float):
            Probabilidad de mutar cada gen de manera independiente.
        sigma (float):
            Desviación estándar de la perturbación gaussiana N(0, sigma).

    Retorna:
        list[float]: Nuevo individuo mutado (copia del original con posibles
        modificaciones en algunos genes).
    """
    nuevo: list[float] = []

    for i, valor in enumerate(individuo):
        if random.random() < probabilidad_mutacion:
            perturbacion = random.gauss(0, sigma)
            valor_mutado = valor + perturbacion
            minimo, maximo = LIMITES[i]
            valor_mutado = recortar(valor_mutado, minimo, maximo)

            nuevo.append(valor_mutado)
        else:
            # Sin mutación: se copia el valor original
            nuevo.append(valor)

    return nuevo


# -----------------------------------------------------------------------------
# 5. Bucle de simulación de mutaciones
#
# La función `ejecutar_mutaciones` no implementa un algoritmo genético completo,
# sino un experimento controlado para observar cómo opera el operador de
# mutación a lo largo de varias generaciones:
#
#     1) Se genera una población inicial de individuos reales.
#     2) En cada generación, se muta cada individuo de la población.
#     3) Si un individuo cambia (es decir, al menos un gen se modifica),
#        se imprime en pantalla el estado "antes" y "después" de la mutación.
#
# Este procedimiento es útil para:
#     - Verificar que la mutación está funcionando.
#     - Visualizar los cambios en los genes respetando los límites.
#     - Analizar el efecto de los parámetros `probabilidad_mutacion` y `sigma`.
# -----------------------------------------------------------------------------
def ejecutar_mutaciones(
    generaciones: int = 50,
    tamano_poblacion: int = 1000,
    probabilidad_mutacion: float = 0.1,
    sigma: float = 1.0,
) -> None:
    """
    Ejecuta un experimento de mutación sobre varias generaciones.

    En cada generación, se aplica mutación gaussiana a todos los individuos
    de la población. Si un individuo cambia, se imprimen sus valores antes
    y después de la mutación.

    Parámetros:
        generaciones (int):
            Número de generaciones a simular.
        tamano_poblacion (int):
            Número de individuos en la población.
        probabilidad_mutacion (float):
            Probabilidad de mutación por gen.
        sigma (float):
            Desviación estándar de la perturbación gaussiana aplicada
            a cada gen que se muta.
    """
    # 1) Generar población inicial
    poblacion = poblacion_inicial_real(tamano_poblacion)

    # 2) Bucle de generaciones
    for gen in range(1, generaciones + 1):
        print(f"\n=== GENERACIÓN {gen} ===")

        nueva_poblacion: list[list[float]] = []

        for idx, ind in enumerate(poblacion):
            original = ind
            mutado = mutar_individuo_real(
                original,
                probabilidad_mutacion=probabilidad_mutacion,
                sigma=sigma,
            )

            # Detectar si hubo un cambio real en algún gen (tolerancia numérica)
            if any(abs(o - m) > 1e-9 for o, m in zip(original, mutado)):
                print(f"Gen {gen:02d}, Ind {idx:04d}:")

                print("  Antes:")
                print(f"    Suero:                 {original[0]:.3f} g")
                print(f"    Avena:                 {original[1]:.3f} g")
                print(f"    Mantequilla Almendra:  {original[2]:.3f} g")
                print(f"    Azúcar:                {original[3]:.3f} g")

                print("  Después:")
                print(f"    Suero:                 {mutado[0]:.3f} g")
                print(f"    Avena:                 {mutado[1]:.3f} g")
                print(f"    Mantequilla Almendra:  {mutado[2]:.3f} g")
                print(f"    Azúcar:                {mutado[3]:.3f} g")

                print()  # línea en blanco para separar individuos

            nueva_poblacion.append(mutado)

        # La nueva población se convierte en la población actual
        poblacion = nueva_poblacion


if __name__ == "__main__":
    ejecutar_mutaciones()
