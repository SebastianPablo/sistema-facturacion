# 🚀 Deploy en Heroku - Guía Completa

## 📋 Requisitos Previos
- Cuenta en Heroku (gratuita)
- Git instalado
- Heroku CLI instalado

## 🔧 Pasos para Deploy

### 1. Instalar Heroku CLI
```bash
# Descargar desde: https://devcenter.heroku.com/articles/heroku-cli
# O usar winget en Windows:
winget install Heroku.HerokuCLI
```

### 2. Configurar el Proyecto
```bash
# Inicializar Git (si no está)
git init
git add .
git commit -m "Sistema de facturación completo"

# Login en Heroku
heroku login

# Crear aplicación
heroku create tu-sistema-facturacion

# Configurar variables de entorno
heroku config:set SECRET_KEY=tu_secret_key_aqui
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=tu-sistema-facturacion.herokuapp.com
heroku config:set DATABASE_URL=postgres://user:pass@host:port/db
```

### 3. Archivos Necesarios
- ✅ `Procfile` (ya existe)
- ✅ `requirements.txt` (ya existe)
- ✅ `runtime.txt` (ya existe)

### 4. Deploy
```bash
# Subir código
git push heroku main

# Ejecutar migraciones
heroku run python manage.py migrate

# Crear superusuario
heroku run python manage.py createsuperuser

# Abrir aplicación
heroku open
```

## 💰 Costos
- **Gratis**: 550 horas/mes (suficiente para pruebas)
- **Dormir**: Después de 30 min sin uso
- **Base de datos**: PostgreSQL gratis incluido

## 🔗 URL Final
`https://tu-sistema-facturacion.herokuapp.com`
