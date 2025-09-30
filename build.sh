#!/bin/bash
# Script de build para Render

echo "🔧 Instalando dependencias..."
pip install -r requirements.txt

echo "🗄️ Configurando base de datos..."
python manage.py migrate --noinput

echo "📁 Recopilando archivos estáticos..."
python manage.py collectstatic --noinput

echo "✅ Build completado!"
