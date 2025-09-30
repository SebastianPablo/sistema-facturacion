# 🎨 Deploy en Render - Guía Simple

## 📋 Ventajas de Render
- ✅ Deploy desde GitHub en 1 click
- ✅ Base de datos PostgreSQL gratis
- ✅ SSL automático
- ✅ 750 horas gratis/mes

## 🔧 Pasos para Deploy

### 1. Preparar Archivos
Crear `render.yaml`:
```yaml
services:
  - type: web
    name: sistema-facturacion
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn aguas_del_valle.wsgi --log-file -
    envVars:
      - key: SECRET_KEY
        generateValue: true
      - key: DEBUG
        value: False
      - key: ALLOWED_HOSTS
        value: tu-app.onrender.com
```

### 2. Subir a GitHub
```bash
git add .
git commit -m "Listo para Render"
git push origin main
```

### 3. Deploy en Render
1. Ir a [render.com](https://render.com)
2. Conectar con GitHub
3. Seleccionar "New Web Service"
4. Elegir tu repositorio
5. Render detectará Django automáticamente

### 4. Configurar Base de Datos
1. Crear PostgreSQL database en Render
2. Copiar DATABASE_URL
3. Agregar a variables de entorno

## 💰 Costos
- **Gratis**: 750 horas/mes
- **Dormir**: Después de 15 min sin uso

## 🔗 URL Final
`https://tu-app.onrender.com`
