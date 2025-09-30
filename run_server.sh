#!/bin/bash

echo "Iniciando servidor Django - Prueba"
echo

# Activar entorno virtual si existe
if [ -f "venv/bin/activate" ]; then
    echo "Activando entorno virtual..."
    source venv/bin/activate
fi

# Instalar dependencias si es necesario
echo "Verificando dependencias..."
pip install -r requirements.txt

# Ejecutar migraciones
echo "Ejecutando migraciones..."
python manage.py makemigrations
python manage.py migrate

# Crear superusuario si no existe
echo "Creando superusuario..."
python manage.py createsuperuser --noinput --username admin --email admin@aguasdelvalle.cl 2>/dev/null || echo "Superusuario ya existe"

# Iniciar servidor
echo
echo "Iniciando servidor en http://127.0.0.1:8000/"
echo "Presiona Ctrl+C para detener el servidor"
echo
python manage.py runserver
