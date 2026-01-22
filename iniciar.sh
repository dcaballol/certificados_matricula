#!/bin/bash

echo "========================================"
echo "Sistema de Certificados de Matrícula"
echo "SLEP Santa Corina"
echo "========================================"
echo ""

# Verificar si existe el entorno virtual
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
    echo ""
fi

# Activar entorno virtual
echo "Activando entorno virtual..."
source venv/bin/activate
echo ""

# Instalar dependencias
echo "Instalando dependencias..."
pip install -r requirements.txt
echo ""

# Ejecutar la aplicación
echo "Iniciando aplicación..."
echo "La aplicación se abrirá en tu navegador"
echo "Presiona Ctrl+C para detener la aplicación"
echo ""
streamlit run app.py
