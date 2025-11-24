#!/bin/sh

# Obtener el directorio donde está el script y movernos ahí
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

echo "Ejecutando desde: $SCRIPT_DIR"

# Nombre del entorno virtual
VENV_DIR=".venv"
OUTPUT_DIR="outputs"

echo "Verificando entorno virtual..."

# Crear entorno virtual si no existe
if [ ! -d "$VENV_DIR" ]; then
    echo "No existe $VENV_DIR. Creando entorno virtual..."
    python3 -m venv "$VENV_DIR"
else
    echo "El entorno virtual ya existe."
fi

# Activar entorno virtual
echo "Activando entorno virtual..."
. "$VENV_DIR/bin/activate"

if [ -z "$VIRTUAL_ENV" ]; then
    echo "ERROR: No se pudo activar el entorno virtual."
    exit 1
fi

echo "Entorno virtual activado en: $VIRTUAL_ENV"

# Instalar dependencias
echo "Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# Ejecutar scripts
echo "Ejecutando Tarea2/AlgoritmoGenetico.py..."
python ./Tarea2/AlgoritmoGenetico.py > tarea1.log

echo "Ejecutando Tarea2/graph_gen.py..."
python ./Tarea2/graph_gen.py &   # en segundo plano
GRAPH_PID=$!

echo "Ejecutando Tarea3/OptimizacionDimensionesCaja.py..."
python ./Tarea3/OptimizacionDimensionesCaja.py > tarea3.log

echo "Ejecutando Tarea4/BarraDeProteina.py..."
python ./Tarea4/BarraDeProteina.py > tarea4.log

# Esperar a que termine graph_gen.py antes de mover outputs
wait "$GRAPH_PID"

echo "Creando directorio de outputs..."
mkdir -p "$OUTPUT_DIR"

echo "Moviendo logs a $OUTPUT_DIR..."
mv tarea1.log tarea3.log tarea4.log "$OUTPUT_DIR"/ 2>/dev/null

echo "Moviendo CSVs a $OUTPUT_DIR..."
mv ./*.csv "$OUTPUT_DIR"/ 2>/dev/null

echo "Moviendo PNGs a $OUTPUT_DIR..."
mv ./*.png "$OUTPUT_DIR"/ 2>/dev/null

echo "Proceso completado. Outputs en: $OUTPUT_DIR"

