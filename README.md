# Sistema de Facturación - Prueba

Un sistema web completo para la gestión de facturación de servicios de agua, desarrollado con Django.

## 🚀 Características

- **Gestión de Clientes**: Registro y administración de clientes
- **Mediciones**: Registro de consumo de agua con cálculo automático
- **Boletas**: Generación de boletas en PDF con envío por correo
- **Avisos**: Sistema de notificaciones por correo electrónico
- **Interfaz Moderna**: Diseño responsive con Bootstrap 5

## 📋 Requisitos

- Python 3.8+
- Django 4.2+
- SQLite (incluido con Python)

## 🛠️ Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd aguas-del-valle
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar base de datos**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Crear superusuario (opcional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Ejecutar servidor**
   ```bash
   python manage.py runserver
   ```

7. **Acceder al sistema**
   - Aplicación: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/

## 📊 Estructura de la Base de Datos

### Modelos Principales

- **Cliente**: Información personal y de contacto
- **Medición**: Registro de consumo de agua
- **Boleta**: Facturas generadas
- **Aviso**: Notificaciones a clientes

### Relaciones

- Un cliente puede tener múltiples mediciones
- Una medición genera una boleta
- Un cliente puede recibir múltiples avisos

## 🔧 Configuración de Correo

Para habilitar el envío de correos, edita `aguas_del_valle/settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tu-email@gmail.com'
EMAIL_HOST_PASSWORD = 'tu-contraseña'
```

## 📱 Funcionalidades

### Gestión de Clientes
- Registro de nuevos clientes
- Listado y búsqueda de clientes
- Detalle completo con historial

### Mediciones
- Registro de lecturas del medidor
- Cálculo automático de consumo
- Tarifa: $500 CLP por m³

### Boletas
- Generación automática de PDFs
- Envío por correo electrónico
- Numeración automática

### Avisos
- Diferentes tipos de notificaciones
- Envío masivo por correo
- Seguimiento de estado

## 🎨 Interfaz de Usuario

- **Bootstrap 5**: Diseño moderno y responsive
- **Bootstrap Icons**: Iconografía consistente
- **Navegación Intuitiva**: Menús claros y accesibles
- **Dashboard**: Estadísticas en tiempo real

## 📄 Generación de PDFs

El sistema utiliza ReportLab para generar boletas en PDF con:
- Logo y datos de la empresa
- Información del cliente
- Detalles de consumo y tarifas
- Formato profesional

## 🔐 Seguridad

- Validación de formularios
- Protección CSRF
- Sanitización de datos
- Autenticación de usuarios

## 🚀 Despliegue

Para producción, considera:

1. **Configuración de Base de Datos**
   - PostgreSQL o MySQL para producción
   - Configuración de variables de entorno

2. **Servidor Web**
   - Nginx + Gunicorn
   - Configuración SSL

3. **Variables de Entorno**
   ```bash
   SECRET_KEY=tu-secret-key
   DEBUG=False
   ALLOWED_HOSTS=tu-dominio.com
   ```

## 📞 Soporte

Para soporte técnico o consultas:
- Email: soporte@aguasdelvalle.cl
- Teléfono: +56 9 1234 5678

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

---

**Prueba** - Sistema de Facturación v1.0
