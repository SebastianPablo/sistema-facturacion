# 🚀 Deploy Manual a Heroku - Sin CLI

## 📋 Pasos para Deploy Manual

### 1. 🌐 Crear Cuenta en Heroku
- Ve a: https://heroku.com
- Regístrate (gratis)
- Confirma tu email

### 2. 📁 Subir Código a GitHub
```bash
# Inicializar Git
git init
git add .
git commit -m "Sistema de facturación"

# Crear repositorio en GitHub
# Subir código
git remote add origin https://github.com/tu-usuario/tu-repositorio.git
git push -u origin main
```

### 3. 🏗️ Crear App en Heroku
1. Ve a: https://dashboard.heroku.com
2. Clic en "New" → "Create new app"
3. Nombre: `tu-sistema-facturacion` (debe ser único)
4. Región: United States
5. Clic en "Create app"

### 4. 🔗 Conectar con GitHub
1. En tu app, ve a "Deploy" tab
2. En "Deployment method", selecciona "GitHub"
3. Conecta tu cuenta de GitHub
4. Selecciona tu repositorio
5. Clic en "Connect"

### 5. ⚙️ Configurar Variables
En "Settings" → "Config Vars", agregar:

```
SECRET_KEY = tu_secret_key_aqui
DEBUG = False
ALLOWED_HOSTS = tu-sistema-facturacion.herokuapp.com
DJANGO_SETTINGS_MODULE = aguas_del_valle.settings_production
```

### 6. 🗄️ Agregar Base de Datos
1. En "Resources" tab
2. Buscar "Heroku Postgres"
3. Clic en "Add-ons"
4. Seleccionar "Hobby Dev" (gratis)
5. Clic en "Submit Order Form"

### 7. 🚀 Deploy
1. En "Deploy" tab
2. Clic en "Deploy Branch"
3. Esperar a que termine

### 8. 🗄️ Configurar Base de Datos
1. En "More" → "Run console"
2. Ejecutar:
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 9. 🌐 Abrir App
- Clic en "Open app"
- URL: `https://tu-sistema-facturacion.herokuapp.com`

## 🎯 Resultado Final
- ✅ App funcionando en internet
- ✅ Base de datos PostgreSQL
- ✅ SSL automático (HTTPS)
- ✅ Deploy automático desde GitHub

## 📱 Para Compartir
```
URL: https://tu-sistema-facturacion.herokuapp.com
Usuario: admin
Password: admin123
```
