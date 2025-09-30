#!/bin/bash
# Script de build para Render

echo "🔧 Instalando dependencias..."
pip install -r requirements.txt

echo "🗄️ Configurando base de datos..."
python3 manage.py migrate --noinput

echo "📁 Recopilando archivos estáticos..."
python3 manage.py collectstatic --noinput

echo "✅ Build completado!"
