#!/usr/bin/env python
"""
Script para configurar la base de datos PostgreSQL.
"""

import os
import subprocess
import sys
from pathlib import Path

def check_postgresql():
    """Verificar si PostgreSQL está instalado."""
    try:
        result = subprocess.run(['psql', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ PostgreSQL encontrado: {result.stdout.strip()}")
            return True
        else:
            print("❌ PostgreSQL no encontrado")
            return False
    except FileNotFoundError:
        print("❌ PostgreSQL no está instalado")
        return False

def create_database():
    """Crear base de datos para el sistema."""
    db_name = "facturacion_db"
    db_user = "facturacion_user"
    db_password = "facturacion_secure_2024"
    
    print(f"🔧 Creando base de datos: {db_name}")
    
    # Comandos SQL para crear la base de datos
    sql_commands = [
        f"CREATE DATABASE {db_name};",
        f"CREATE USER {db_user} WITH PASSWORD '{db_password}';",
        f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user};",
        f"ALTER USER {db_user} CREATEDB;"
    ]
    
    try:
        for command in sql_commands:
            result = subprocess.run([
                'psql', '-U', 'postgres', '-c', command
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"⚠️  Advertencia: {result.stderr}")
            else:
                print(f"✅ Comando ejecutado: {command}")
        
        print("✅ Base de datos creada exitosamente")
        
        # Actualizar archivo .env
        update_env_file(db_name, db_user, db_password)
        
    except Exception as e:
        print(f"❌ Error creando base de datos: {e}")
        print("💡 Instrucciones manuales:")
        print(f"1. Abre psql: psql -U postgres")
        print(f"2. Ejecuta: CREATE DATABASE {db_name};")
        print(f"3. Ejecuta: CREATE USER {db_user} WITH PASSWORD '{db_password}';")
        print(f"4. Ejecuta: GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user};")

def update_env_file(db_name, db_user, db_password):
    """Actualizar archivo .env con configuración de base de datos."""
    env_file = Path('.env')
    
    if env_file.exists():
        # Leer archivo existente
        with open(env_file, 'r') as f:
            content = f.read()
        
        # Actualizar configuración de base de datos
        lines = content.split('\n')
        updated_lines = []
        
        for line in lines:
            if line.startswith('DB_NAME='):
                updated_lines.append(f'DB_NAME={db_name}')
            elif line.startswith('DB_USER='):
                updated_lines.append(f'DB_USER={db_user}')
            elif line.startswith('DB_PASSWORD='):
                updated_lines.append(f'DB_PASSWORD={db_password}')
            else:
                updated_lines.append(line)
        
        # Escribir archivo actualizado
        with open(env_file, 'w') as f:
            f.write('\n'.join(updated_lines))
        
        print("✅ Archivo .env actualizado con configuración de base de datos")

def install_requirements():
    """Instalar dependencias adicionales para PostgreSQL."""
    requirements = [
        'psycopg2-binary==2.9.7',
        'python-decouple==3.8'
    ]
    
    print("📦 Instalando dependencias para PostgreSQL...")
    
    for req in requirements:
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', req], check=True)
            print(f"✅ {req} instalado")
        except subprocess.CalledProcessError:
            print(f"❌ Error instalando {req}")

def create_migration():
    """Crear migraciones para los nuevos índices."""
    print("🔄 Creando migraciones...")
    
    try:
        # Crear migraciones
        subprocess.run(['python', 'manage.py', 'makemigrations'], check=True)
        print("✅ Migraciones creadas")
        
        # Aplicar migraciones
        subprocess.run(['python', 'manage.py', 'migrate'], check=True)
        print("✅ Migraciones aplicadas")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en migraciones: {e}")

def main():
    """Función principal."""
    print("🗄️  Configurando base de datos PostgreSQL...")
    
    # Verificar PostgreSQL
    if not check_postgresql():
        print("\n📋 Para instalar PostgreSQL:")
        print("1. Windows: https://www.postgresql.org/download/windows/")
        print("2. macOS: brew install postgresql")
        print("3. Ubuntu: sudo apt install postgresql postgresql-contrib")
        return
    
    # Instalar dependencias
    install_requirements()
    
    # Crear base de datos
    create_database()
    
    # Crear migraciones
    create_migration()
    
    print("\n✅ Configuración de base de datos completada!")
    print("\n📋 Próximos pasos:")
    print("1. Verifica la conexión: python manage.py dbshell")
    print("2. Crea un superusuario: python manage.py createsuperuser")
    print("3. Ejecuta el servidor: python manage.py runserver")

if __name__ == "__main__":
    main()
