@echo off
echo ========================================
echo Sistema de Certificados de Matricula
echo SLEP Santa Corina
echo ========================================
echo.

REM Verificar si existe el entorno virtual
if not exist "venv\" (
    echo Creando entorno virtual...
    python -m venv venv
    echo.
)

REM Activar entorno virtual
echo Activando entorno virtual...
call venv\Scripts\activate.bat
echo.

REM Instalar dependencias
echo Instalando dependencias...
pip install -r requirements.txt
echo.

REM Ejecutar la aplicacion
echo Iniciando aplicacion...
echo La aplicacion se abrira en tu navegador
echo Presiona Ctrl+C para detener la aplicacion
echo.
streamlit run app.py

pause
