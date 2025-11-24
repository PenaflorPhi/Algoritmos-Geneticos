import csv

import matplotlib.pyplot as plt

generaciones = []
mejor_aptitud = []
aptitud_promedio = []

with open("./algoritmo_genetico_historial.csv", newline="", encoding="utf-8") as f:
    lector = csv.DictReader(f)
    for fila in lector:
        generaciones.append(int(fila["generacion"]))
        mejor_aptitud.append(float(fila["mejor_aptitud"]))
        aptitud_promedio.append(float(fila["aptitud_promedio"]))

plt.plot(generaciones, mejor_aptitud, label="Mejor aptitud")
plt.plot(generaciones, aptitud_promedio, label="Aptitud promedio")
plt.xlabel("Generación")
plt.ylabel("Aptitud")
plt.title("Evolución de la aptitud en el algoritmo genético")
plt.legend()
plt.grid(True)

plt.savefig("evolucion_aptitud.png", dpi=300, bbox_inches="tight")
