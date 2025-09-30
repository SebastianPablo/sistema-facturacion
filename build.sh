#!/bin/bash
# Script de build para Render

echo "🔧 Instalando dependencias..."
pip install -r requirements.txt

echo "🗄️ Configurando base de datos..."
python manage.py migrate

echo "👤 Creando superusuario..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@test.com', 'admin123') if not User.objects.filter(username='admin').exists() else None" | python manage.py shell

echo "📁 Recopilando archivos estáticos..."
python manage.py collectstatic --noinput

echo "✅ Build completado!"
