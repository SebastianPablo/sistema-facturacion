# 🚂 Deploy en Railway - Guía Rápida

## 📋 Ventajas de Railway
- ✅ Deploy automático desde GitHub
- ✅ Base de datos PostgreSQL incluida
- ✅ SSL automático
- ✅ $5 USD gratis al mes

## 🔧 Pasos para Deploy

### 1. Preparar el Proyecto
```bash
# Crear archivo railway.json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn aguas_del_valle.wsgi --log-file -",
    "healthcheckPath": "/"
  }
}
```

### 2. Subir a GitHub
```bash
git add .
git commit -m "Sistema listo para Railway"
git push origin main
```

### 3. Conectar con Railway
1. Ir a [railway.app](https://railway.app)
2. Conectar con GitHub
3. Seleccionar tu repositorio
4. Railway detectará Django automáticamente

### 4. Configurar Variables
En Railway Dashboard:
```
SECRET_KEY=tu_secret_key_aqui
DEBUG=False
ALLOWED_HOSTS=tu-app.railway.app
DATABASE_URL=postgresql://...
```

## 💰 Costos
- **Gratis**: $5 USD de crédito mensual
- **Suficiente**: Para pruebas y demos

## 🔗 URL Final
`https://tu-app.railway.app`
