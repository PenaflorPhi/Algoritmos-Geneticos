import random

LIMITES = [
    (10.0, 50.0),  # proteína de suero
    (20.0, 100.0),  # avena
    (5.0, 30.0),  # mantequilla de almendra
    (0.0, 20.0),  # azúcar
]


def individuo_aleatorio() -> list[float]:
    return [
        random.uniform(10, 50),  # proteína de suero
        random.uniform(20, 100),  # avena
        random.uniform(5, 30),  # mantequilla de almendra
        random.uniform(0, 20),  # azúcar
    ]


def poblacion_inicial_real(tamano: int) -> list[list[float]]:
    return [individuo_aleatorio() for _ in range(tamano)]


def recortar(valor: float, minimo: float, maximo: float) -> float:
    return max(minimo, min(maximo, valor))


def mutar_individuo_real(
    individuo: list[float],
    probabilidad_mutacion: float = 0.1,
    sigma: float = 1.0,
) -> list[float]:
    nuevo: list[float] = []

    for i, valor in enumerate(individuo):
        if random.random() < probabilidad_mutacion:
            perturbacion = random.gauss(0, sigma)
            valor_mutado = valor + perturbacion
            minimo, maximo = LIMITES[i]
            valor_mutado = recortar(valor_mutado, minimo, maximo)
            nuevo.append(valor_mutado)
        else:
            nuevo.append(valor)

    return nuevo


def ejecutar_mutaciones(
    generaciones: int = 50,
    tamano_poblacion: int = 1000,
    probabilidad_mutacion: float = 0.1,
    sigma: float = 1.0,
) -> None:
    poblacion = poblacion_inicial_real(tamano_poblacion)

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

            # Detectar si hubo un cambio real
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

                print()  # línea en blanco

            nueva_poblacion.append(mutado)

        poblacion = nueva_poblacion


if __name__ == "__main__":
    ejecutar_mutaciones()
