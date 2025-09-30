from django.db import models
from django.core.validators import EmailValidator
from django.utils import timezone


class Cliente(models.Model):
    """Modelo para almacenar información de clientes"""
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200, verbose_name="Nombre Completo", db_index=True)
    direccion = models.TextField(verbose_name="Dirección")
    email = models.EmailField(validators=[EmailValidator()], verbose_name="Correo Electrónico", unique=True, db_index=True)
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono", db_index=True)
    fecha_registro = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Registro", db_index=True)
    activo = models.BooleanField(default=True, verbose_name="Cliente Activo", db_index=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nombre']
        indexes = [
            models.Index(fields=['activo', 'fecha_registro']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return f"{self.nombre} - {self.email}"


class Medicion(models.Model):
    """Modelo para almacenar mediciones de consumo de agua"""
    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente", db_index=True)
    fecha = models.DateField(verbose_name="Fecha de Medición", db_index=True)
    consumo_m3 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Consumo (m³)", db_index=True)
    lectura_anterior = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Lectura Anterior")
    lectura_actual = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Lectura Actual")
    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones")
    fecha_registro = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Registro", db_index=True)

    class Meta:
        verbose_name = "Medición"
        verbose_name_plural = "Mediciones"
        ordering = ['-fecha']
        indexes = [
            models.Index(fields=['cliente', 'fecha']),
            models.Index(fields=['fecha', 'consumo_m3']),
            models.Index(fields=['fecha_registro']),
        ]

    def __str__(self):
        return f"{self.cliente.nombre} - {self.fecha} - {self.consumo_m3} m³"

    @property
    def monto_calculado(self):
        """Calcula el monto basado en el consumo (500 CLP por m³)"""
        return self.consumo_m3 * 500


class Boleta(models.Model):
    """Modelo para almacenar boletas de facturación"""
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('pagada', 'Pagada'),
        ('vencida', 'Vencida'),
        ('cancelada', 'Cancelada'),
    ]

    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente", db_index=True)
    medicion = models.ForeignKey(Medicion, on_delete=models.CASCADE, verbose_name="Medición", db_index=True)
    fecha_emision = models.DateField(default=timezone.now, verbose_name="Fecha de Emisión", db_index=True)
    fecha_vencimiento = models.DateField(verbose_name="Fecha de Vencimiento", db_index=True)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto Total", db_index=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente', verbose_name="Estado", db_index=True)
    numero_boleta = models.CharField(max_length=20, unique=True, verbose_name="Número de Boleta", db_index=True)
    fecha_registro = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Registro", db_index=True)

    class Meta:
        verbose_name = "Boleta"
        verbose_name_plural = "Boletas"
        ordering = ['-fecha_emision']
        indexes = [
            models.Index(fields=['cliente', 'estado']),
            models.Index(fields=['fecha_emision', 'estado']),
            models.Index(fields=['numero_boleta']),
            models.Index(fields=['fecha_vencimiento']),
        ]

    def __str__(self):
        return f"Boleta #{self.numero_boleta} - {self.cliente.nombre} - ${self.monto_total}"

    def save(self, *args, **kwargs):
        if not self.numero_boleta:
            # Generar número de boleta automáticamente
            import datetime
            year = datetime.datetime.now().year
            month = datetime.datetime.now().month
            count = Boleta.objects.filter(fecha_emision__year=year, fecha_emision__month=month).count() + 1
            self.numero_boleta = f"B{year}{month:02d}{count:04d}"
        super().save(*args, **kwargs)


class Aviso(models.Model):
    """Modelo para almacenar avisos a clientes"""
    TIPO_AVISO_CHOICES = [
        ('corte_programado', 'Corte Programado'),
        ('mantenimiento', 'Mantenimiento'),
        ('cambio_tarifa', 'Cambio de Tarifa'),
        ('informacion_general', 'Información General'),
        ('recordatorio_pago', 'Recordatorio de Pago'),
    ]

    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente", db_index=True)
    fecha = models.DateTimeField(default=timezone.now, verbose_name="Fecha del Aviso", db_index=True)
    tipo_aviso = models.CharField(max_length=30, choices=TIPO_AVISO_CHOICES, verbose_name="Tipo de Aviso", db_index=True)
    titulo = models.CharField(max_length=200, verbose_name="Título", db_index=True)
    mensaje = models.TextField(verbose_name="Mensaje")
    enviado = models.BooleanField(default=False, verbose_name="Enviado", db_index=True)
    fecha_envio = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de Envío", db_index=True)

    class Meta:
        verbose_name = "Aviso"
        verbose_name_plural = "Avisos"
        ordering = ['-fecha']
        indexes = [
            models.Index(fields=['cliente', 'enviado']),
            models.Index(fields=['tipo_aviso', 'fecha']),
            models.Index(fields=['enviado', 'fecha']),
        ]

    def __str__(self):
        return f"{self.titulo} - {self.cliente.nombre}"
