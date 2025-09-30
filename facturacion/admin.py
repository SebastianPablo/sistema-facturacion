from django.contrib import admin
from .models import Cliente, Medicion, Boleta, Aviso


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'email', 'telefono', 'fecha_registro', 'activo']
    list_filter = ['activo', 'fecha_registro']
    search_fields = ['nombre', 'email', 'direccion']
    list_editable = ['activo']


@admin.register(Medicion)
class MedicionAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'fecha', 'consumo_m3', 'monto_calculado', 'fecha_registro']
    list_filter = ['fecha', 'cliente']
    search_fields = ['cliente__nombre', 'observaciones']
    date_hierarchy = 'fecha'


@admin.register(Boleta)
class BoletaAdmin(admin.ModelAdmin):
    list_display = ['numero_boleta', 'cliente', 'fecha_emision', 'monto_total', 'estado']
    list_filter = ['estado', 'fecha_emision']
    search_fields = ['numero_boleta', 'cliente__nombre']
    date_hierarchy = 'fecha_emision'


@admin.register(Aviso)
class AvisoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'cliente', 'tipo_aviso', 'fecha', 'enviado']
    list_filter = ['tipo_aviso', 'enviado', 'fecha']
    search_fields = ['titulo', 'mensaje', 'cliente__nombre']
    date_hierarchy = 'fecha'
