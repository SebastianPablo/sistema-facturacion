# 🌐 Sistema de Facturación - Instrucciones para Usuarios

## 🔗 Acceso al Sistema
**URL:** `https://tu-sistema-facturacion.herokuapp.com`

## 👤 Credenciales de Prueba
- **Usuario:** `demo`
- **Contraseña:** `demo123`

## 🎯 Funcionalidades Disponibles

### 👥 Gestión de Clientes
- ✅ **Crear cliente** - Registro completo
- ✅ **Ver clientes** - Lista con información
- ✅ **Editar cliente** - Modificar datos
- ✅ **Eliminar cliente** - Con confirmación

### 📊 Gestión de Mediciones
- ✅ **Registrar medición** - Con cálculo automático
- ✅ **Ver mediciones** - Lista completa
- ✅ **Editar medición** - Modificar lecturas
- ✅ **Eliminar medición** - Con confirmación

### 🧾 Gestión de Boletas
- ✅ **Generar boleta** - Desde medición
- ✅ **Ver PDF** - Descargar boleta
- ✅ **Enviar por email** - Notificación automática
- ✅ **Cambiar estado** - Pagada/Vencida/Cancelada

### 📢 Gestión de Avisos
- ✅ **Crear aviso** - Diferentes tipos
- ✅ **Enviar aviso** - Por email al cliente
- ✅ **Ver avisos** - Lista completa

### 🔍 Funcionalidades Adicionales
- ✅ **Búsqueda global** - Clientes, boletas, avisos
- ✅ **Reportes** - Estadísticas y análisis
- ✅ **Dashboard** - Vista general del sistema

## 🎮 Flujo de Prueba Recomendado

### 1. **Crear Cliente**
1. Ir a "Clientes" → "Nuevo Cliente"
2. Llenar formulario completo
3. Hacer clic en "Guardar Cliente"

### 2. **Registrar Medición**
1. Ir a "Mediciones" → "Nueva Medición"
2. Seleccionar cliente
3. Ingresar lecturas del medidor
4. Hacer clic en "Guardar Medición"

### 3. **Generar Boleta**
1. Ir a "Boletas" → "Generar Boleta"
2. Seleccionar cliente y medición
3. Hacer clic en "Generar Boleta"

### 4. **Ver PDF y Enviar**
1. En detalle del cliente, hacer clic en "Ver PDF"
2. Hacer clic en "Enviar por Email"
3. Verificar en consola del servidor

### 5. **Crear Aviso**
1. Ir a "Avisos" → "Nuevo Aviso"
2. Seleccionar cliente y tipo
3. Escribir mensaje
4. Hacer clic en "Crear Aviso"

## 📱 Características Técnicas

### 🎨 Interfaz
- ✅ **Responsive** - Funciona en móvil y desktop
- ✅ **Bootstrap 5** - Diseño moderno
- ✅ **Iconos** - Navegación intuitiva

### 🔒 Seguridad
- ✅ **Validación** - Formularios seguros
- ✅ **Sanitización** - Entrada de datos limpia
- ✅ **Headers** - Seguridad HTTP

### 📊 Base de Datos
- ✅ **PostgreSQL** - Base de datos robusta
- ✅ **Índices** - Consultas optimizadas
- ✅ **Relaciones** - Datos estructurados

## 🆘 Soporte

### ❓ Problemas Comunes
1. **Error 500** - Recargar página
2. **Formulario no envía** - Verificar campos requeridos
3. **PDF no se genera** - Verificar que existe la medición

### 🔧 Información Técnica
- **Framework:** Django 4.2.7
- **Base de datos:** PostgreSQL
- **Hosting:** Heroku
- **SSL:** Automático

## 📞 Contacto
Para soporte técnico o preguntas sobre el sistema.
