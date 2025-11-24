# Tarea de Algoritmos Genéticos

Este repositorio contiene la implementación de diversas actividades relacionadas con algoritmos genéticos, incluyendo generación de poblaciones, operadores evolutivos, experimentos y problemas de optimización.
Todas las tareas pueden ejecutarse mediante un único script (`run.sh`) que automatiza la preparación del entorno y la ejecución.

---

## Características principales

- Creación y activación automática de un entorno virtual de Python.
- Instalación de todas las dependencias necesarias mediante `pip`.
- Ejecución secuencial de los scripts correspondientes a cada tarea.
- Almacenamiento de resultados (gráficas, datos y logs) en el directorio `outputs/`.

---

## Requisitos

El script `run.sh` se encarga de gestionar el entorno y las dependencias, por lo que solo necesitas:

- Python 3.12 instalado en el sistema.
- `bash` para ejecutar el script en Linux/macOS (o WSL en Windows).

### Dependencias:
- `matplotlib`

---

## Ejecución

Desde la raíz del proyecto:

```bash
chmod +x run.sh
./run.sh
```

El script realiza lo siguiente:
1. Crea un entorno virtual (.venv/) si no existe.
2. Activa el entorno virtual.
3. Instala las dependencias especificadas en requirements.txt.
4. Ejecuta los distintos módulos de la tarea:
    - Tarea2/AlgoritmoGenetico.py
    - Tarea2/graph_gen.py
    - Tarea3/OptimizacionDimensionesCaja.py
    - Tarea4/BarraDeProteina.py
Guarda todos los resultados generados en `outputs/`.
