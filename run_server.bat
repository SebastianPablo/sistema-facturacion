@echo off
echo Iniciando servidor Django - Prueba
echo.

REM Activar entorno virtual si existe
if exist "venv\Scripts\activate.bat" (
    echo Activando entorno virtual...
    call venv\Scripts\activate.bat
)

REM Instalar dependencias si es necesario
echo Verificando dependencias...
pip install -r requirements.txt

REM Ejecutar migraciones
echo Ejecutando migraciones...
python manage.py makemigrations
python manage.py migrate

REM Crear superusuario si no existe
echo Creando superusuario...
python manage.py createsuperuser --noinput --username admin --email admin@aguasdelvalle.cl || echo Superusuario ya existe

REM Iniciar servidor
echo.
echo Iniciando servidor en http://127.0.0.1:8000/
echo Presiona Ctrl+C para detener el servidor
echo.
python manage.py runserver

pause
