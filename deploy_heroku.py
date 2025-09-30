#!/usr/bin/env python
"""
Script para deploy automático a Heroku
"""

import os
import subprocess
import sys
import secrets

def run_command(command, description):
    """Ejecutar comando y mostrar resultado"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completado")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}: {e.stderr}")
        return None

def check_heroku_cli():
    """Verificar si Heroku CLI está instalado"""
    try:
        subprocess.run(['heroku', '--version'], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def main():
    print("🚀 Deploy Automático a Heroku - Sistema de Facturación")
    print("=" * 60)
    
    # Verificar Heroku CLI
    if not check_heroku_cli():
        print("❌ Heroku CLI no está instalado")
        print("📥 Descarga desde: https://devcenter.heroku.com/articles/heroku-cli")
        print("💡 O ejecuta: winget install Heroku.HerokuCLI")
        return
    
    print("✅ Heroku CLI detectado")
    
    # Solicitar nombre de la app
    app_name = input("\n📝 Ingresa nombre para tu app (debe ser único): ").strip()
    if not app_name:
        print("❌ Nombre de app requerido")
        return
    
    # Generar SECRET_KEY
    secret_key = secrets.token_urlsafe(50)
    print(f"🔑 SECRET_KEY generado: {secret_key[:20]}...")
    
    # Inicializar Git si no existe
    if not os.path.exists('.git'):
        print("📁 Inicializando Git...")
        run_command('git init', 'Inicializar Git')
        run_command('git add .', 'Agregar archivos')
        run_command('git commit -m "Sistema de facturación inicial"', 'Commit inicial')
    
    # Login en Heroku
    print("\n🔐 Iniciando sesión en Heroku...")
    print("💡 Se abrirá el navegador para login")
    if not run_command('heroku login', 'Login en Heroku'):
        return
    
    # Crear aplicación
    print(f"\n🏗️ Creando aplicación: {app_name}")
    if not run_command(f'heroku create {app_name}', 'Crear aplicación'):
        return
    
    # Configurar variables de entorno
    print("\n⚙️ Configurando variables de entorno...")
    commands = [
        f'heroku config:set SECRET_KEY="{secret_key}"',
        'heroku config:set DEBUG=False',
        f'heroku config:set ALLOWED_HOSTS="{app_name}.herokuapp.com"',
        'heroku config:set DJANGO_SETTINGS_MODULE=aguas_del_valle.settings_production'
    ]
    
    for cmd in commands:
        run_command(cmd, f'Configurar: {cmd.split()[-1]}')
    
    # Subir código
    print("\n📤 Subiendo código a Heroku...")
    if not run_command('git add .', 'Agregar cambios'):
        return
    
    if not run_command('git commit -m "Deploy a producción"', 'Commit para deploy'):
        return
    
    if not run_command('git push heroku main', 'Push a Heroku'):
        return
    
    # Configurar base de datos
    print("\n🗄️ Configurando base de datos...")
    run_command('heroku run python manage.py migrate', 'Ejecutar migraciones')
    
    # Crear superusuario
    print("\n👤 Creando usuario administrador...")
    print("💡 Usuario: admin")
    print("💡 Email: admin@test.com")
    print("💡 Password: admin123")
    
    # Crear archivo temporal para superusuario
    with open('create_superuser.py', 'w') as f:
        f.write('''
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@test.com", "admin123")
    print("Superusuario creado: admin/admin123")
else:
    print("Superusuario ya existe")
''')
    
    run_command('heroku run python create_superuser.py', 'Crear superusuario')
    
    # Limpiar archivo temporal
    os.remove('create_superuser.py')
    
    # Abrir aplicación
    print(f"\n🌐 Abriendo aplicación: https://{app_name}.herokuapp.com")
    run_command('heroku open', 'Abrir aplicación')
    
    print("\n" + "=" * 60)
    print("🎉 ¡Deploy completado exitosamente!")
    print(f"🌐 URL: https://{app_name}.herokuapp.com")
    print("👤 Usuario: admin")
    print("🔑 Password: admin123")
    print("\n📋 Para compartir con otros:")
    print(f"   URL: https://{app_name}.herokuapp.com")
    print("   Usuario: admin")
    print("   Password: admin123")
    print("=" * 60)

if __name__ == "__main__":
    main()
