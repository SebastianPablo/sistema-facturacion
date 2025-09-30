# 🐍 Deploy en PythonAnywhere - Más Rápido

## 📋 Ventajas
- ✅ Deploy en 10 minutos
- ✅ Base de datos MySQL incluida
- ✅ SSL automático
- ✅ 100% gratis para demos

## 🔧 Pasos Rápidos

### 1. Crear Cuenta
- Ir a [pythonanywhere.com](https://pythonanywhere.com)
- Registrarse (gratis)

### 2. Subir Archivos
- Usar el editor web de PythonAnywhere
- Subir todos los archivos del proyecto
- O usar Git: `git clone tu-repositorio`

### 3. Configurar Base de Datos
```bash
# En la consola de PythonAnywhere
pip3.10 install --user django
pip3.10 install --user -r requirements.txt

# Configurar base de datos MySQL
python3.10 manage.py migrate
python3.10 manage.py createsuperuser
```

### 4. Configurar Web App
1. Ir a "Web" tab
2. Crear nueva web app
3. Elegir "Manual configuration"
4. Seleccionar Python 3.10
5. Configurar WSGI file

### 5. Variables de Entorno
En el archivo WSGI:
```python
import os
os.environ['SECRET_KEY'] = 'tu_secret_key'
os.environ['DEBUG'] = 'False'
os.environ['ALLOWED_HOSTS'] = 'tu-usuario.pythonanywhere.com'
```

## 💰 Costos
- **Gratis**: Para demos y pruebas
- **Límite**: 1 web app, 1 base de datos

## 🔗 URL Final
`https://tu-usuario.pythonanywhere.com`
