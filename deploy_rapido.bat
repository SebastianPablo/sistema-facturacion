@echo off
echo 🚀 Deploy Rápido a Heroku - Sistema de Facturación
echo.

echo 📋 Paso 1: Instalar Heroku CLI
echo Descarga desde: https://devcenter.heroku.com/articles/heroku-cli
echo O ejecuta: winget install Heroku.HerokuCLI
echo.
pause

echo 📋 Paso 2: Login en Heroku
heroku login
echo.

echo 📋 Paso 3: Crear aplicación
set /p APP_NAME="Ingresa nombre de tu app (debe ser único): "
heroku create %APP_NAME%
echo.

echo 📋 Paso 4: Configurar variables
heroku config:set SECRET_KEY=%RANDOM%%RANDOM%%RANDOM%
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=%APP_NAME%.herokuapp.com
echo.

echo 📋 Paso 5: Subir código
git add .
git commit -m "Sistema listo para producción"
git push heroku main
echo.

echo 📋 Paso 6: Configurar base de datos
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
echo.

echo 📋 Paso 7: Abrir aplicación
heroku open
echo.

echo ✅ ¡Deploy completado!
echo 🌐 Tu sistema está disponible en: https://%APP_NAME%.herokuapp.com
echo.
pause
