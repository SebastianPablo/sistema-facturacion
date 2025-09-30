#!/usr/bin/env python
"""
Script para configurar la seguridad del sistema.
"""

import os
import secrets
import string
from pathlib import Path

def generate_secret_key():
    """Generar una clave secreta segura."""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*(-_=+)"
    return ''.join(secrets.choice(alphabet) for _ in range(50))

def create_env_file():
    """Crear archivo .env con configuración segura."""
    env_content = f"""# Configuración de Seguridad - Sistema de Facturación
SECRET_KEY={generate_secret_key()}
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de Datos
DB_NAME=facturacion_db
DB_USER=facturacion_user
DB_PASSWORD={generate_secret_key()[:20]}
DB_HOST=localhost
DB_PORT=5432

# Correo Electrónico
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

# Redis Cache
REDIS_URL=redis://localhost:6379/1
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Archivo .env creado con configuración segura")

def create_logs_directory():
    """Crear directorio de logs."""
    logs_dir = Path('logs')
    logs_dir.mkdir(exist_ok=True)
    
    # Crear archivo .gitkeep
    (logs_dir / '.gitkeep').touch()
    
    print("✅ Directorio de logs creado")

def create_media_directory():
    """Crear directorio de media con permisos seguros."""
    media_dir = Path('media')
    media_dir.mkdir(exist_ok=True)
    
    # Crear subdirectorios
    (media_dir / 'uploads').mkdir(exist_ok=True)
    (media_dir / 'pdfs').mkdir(exist_ok=True)
    
    print("✅ Directorio de media creado")

def create_staticfiles_directory():
    """Crear directorio de archivos estáticos."""
    staticfiles_dir = Path('staticfiles')
    staticfiles_dir.mkdir(exist_ok=True)
    
    print("✅ Directorio de staticfiles creado")

def setup_permissions():
    """Configurar permisos de archivos."""
    # Archivos que deben ser ejecutables
    executable_files = ['manage.py', 'run_server.sh']
    
    for file in executable_files:
        if os.path.exists(file):
            os.chmod(file, 0o755)
    
    print("✅ Permisos de archivos configurados")

def main():
    """Función principal de configuración."""
    print("🔒 Configurando seguridad del sistema...")
    
    create_env_file()
    create_logs_directory()
    create_media_directory()
    create_staticfiles_directory()
    setup_permissions()
    
    print("\n✅ Configuración de seguridad completada!")
    print("\n📋 Próximos pasos:")
    print("1. Configura tu base de datos PostgreSQL")
    print("2. Configura tu servidor de correo")
    print("3. Actualiza ALLOWED_HOSTS con tu dominio")
    print("4. Configura HTTPS en producción")
    print("5. Revisa los logs regularmente")

if __name__ == "__main__":
    main()
