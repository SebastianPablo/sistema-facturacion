#!/usr/bin/env python
"""
Script para preparar el proyecto para deploy en Heroku
"""

import os
import subprocess
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

def main():
    print("🚀 Preparando Sistema para Deploy en Heroku")
    print("=" * 50)
    
    # Generar SECRET_KEY
    secret_key = secrets.token_urlsafe(50)
    print(f"🔑 SECRET_KEY generado: {secret_key[:20]}...")
    
    # Crear archivo .env para producción
    env_content = f"""SECRET_KEY={secret_key}
DEBUG=False
ALLOWED_HOSTS=tu-app.herokuapp.com
DJANGO_SETTINGS_MODULE=aguas_del_valle.settings_production
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    print("✅ Archivo .env creado")
    
    # Inicializar Git si no existe
    if not os.path.exists('.git'):
        print("📁 Inicializando Git...")
        run_command('git init', 'Inicializar Git')
        run_command('git add .', 'Agregar archivos')
        run_command('git commit -m "Sistema de facturación inicial"', 'Commit inicial')
    else:
        print("✅ Git ya inicializado")
        run_command('git add .', 'Agregar cambios')
        run_command('git commit -m "Preparado para deploy"', 'Commit para deploy')
    
    print("\n" + "=" * 50)
    print("🎉 ¡Proyecto preparado para deploy!")
    print("\n📋 Próximos pasos:")
    print("1. 🌐 Ve a: https://github.com")
    print("2. 📁 Crea un nuevo repositorio")
    print("3. 📤 Sube tu código:")
    print("   git remote add origin https://github.com/tu-usuario/tu-repo.git")
    print("   git push -u origin main")
    print("4. 🏗️ Ve a: https://heroku.com")
    print("5. 🔗 Conecta con GitHub")
    print("6. ⚙️ Configura variables:")
    print(f"   SECRET_KEY = {secret_key}")
    print("   DEBUG = False")
    print("   ALLOWED_HOSTS = tu-app.herokuapp.com")
    print("   DJANGO_SETTINGS_MODULE = aguas_del_valle.settings_production")
    print("\n🌐 Tu app estará en: https://tu-app.herokuapp.com")
    print("=" * 50)

if __name__ == "__main__":
    main()
