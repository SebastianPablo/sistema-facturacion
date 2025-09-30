#!/usr/bin/env python
"""
Script para configurar la base de datos automáticamente
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aguas_del_valle.settings_production')
django.setup()

from django.core.management import execute_from_command_line
from django.contrib.auth import get_user_model

def setup_database():
    """Configurar base de datos y crear superusuario"""
    print("🗄️ Configurando base de datos...")
    
    # Ejecutar migraciones
    execute_from_command_line(['manage.py', 'migrate'])
    print("✅ Migraciones ejecutadas")
    
    # Crear superusuario si no existe
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='admin123'
        )
        print("✅ Superusuario creado: admin/admin123")
    else:
        print("ℹ️ Superusuario ya existe")
    
    print("🎉 Base de datos configurada exitosamente!")

if __name__ == "__main__":
    setup_database()