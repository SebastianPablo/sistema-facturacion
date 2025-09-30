#!/bin/bash
# Script de inicio para Render

echo "🚀 Iniciando aplicación..."

# Crear superusuario si no existe
python3 manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@test.com', 'admin123')
    print('✅ Superusuario creado')
else:
    print('ℹ️ Superusuario ya existe')
"

# Iniciar servidor
echo "🌐 Iniciando servidor..."
python3 -m gunicorn aguas_del_valle.wsgi --log-file - --bind 0.0.0.0:$PORT
