@echo off
echo 🚀 Instalación de Heroku CLI - Sistema de Facturación
echo.

echo 📋 Paso 1: Descargar Heroku CLI
echo.
echo 🌐 Abre tu navegador y ve a:
echo    https://devcenter.heroku.com/articles/heroku-cli
echo.
echo 📥 Descarga el instalador para Windows
echo 💡 Busca "Download and install" y haz clic en "Windows"
echo.
pause

echo 📋 Paso 2: Instalar Heroku CLI
echo.
echo 🔧 Ejecuta el instalador descargado
echo ✅ Acepta todos los términos
echo ✅ Deja todas las opciones por defecto
echo.
pause

echo 📋 Paso 3: Verificar instalación
echo.
echo 🔄 Cerrando y reabriendo PowerShell...
echo 💡 Esto es necesario para que reconozca el comando 'heroku'
echo.
pause

echo 📋 Paso 4: Probar Heroku CLI
echo.
echo 🧪 Ejecutando: heroku --version
heroku --version
echo.

if %errorlevel% equ 0 (
    echo ✅ ¡Heroku CLI instalado correctamente!
    echo.
    echo 🚀 Ahora puedes ejecutar el deploy:
    echo    python deploy_heroku.py
    echo.
) else (
    echo ❌ Heroku CLI no se instaló correctamente
    echo.
    echo 🔧 Soluciones:
    echo    1. Reinicia PowerShell como administrador
    echo    2. Verifica que el instalador se ejecutó completamente
    echo    3. Revisa que Heroku CLI esté en el PATH del sistema
    echo.
)

pause
