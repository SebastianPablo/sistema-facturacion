#!/usr/bin/env python
"""
Script simple para crear datos de muestra básicos.
"""

import os
import sys
import django
from django.utils import timezone
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aguas_del_valle.settings')
django.setup()

from facturacion.models import Cliente, Medicion, Boleta, Aviso

def create_basic_data():
    """Crear datos básicos de muestra."""
    print("🎭 Creando datos básicos de muestra...")
    
    try:
        # Verificar si ya existen datos
        if Cliente.objects.count() > 0:
            print("⚠️  Ya existen datos en la base de datos")
            return
        
        # Crear un cliente de muestra
        cliente = Cliente.objects.create(
            nombre='Juan Pérez',
            email='juan.perez@email.com',
            direccion='Av. Principal 123, Santiago',
            telefono='+56912345678'
        )
        print(f"✅ Cliente creado: {cliente.nombre}")
        
        # Crear una medición
        medicion = Medicion.objects.create(
            cliente=cliente,
            fecha=timezone.now().date(),
            consumo_m3=Decimal('25.5'),
            lectura_anterior=Decimal('100.0'),
            lectura_actual=Decimal('125.5'),
            observaciones='Medición mensual'
        )
        print(f"✅ Medición creada: {medicion.consumo_m3} m³")
        
        # Crear una boleta
        boleta = Boleta.objects.create(
            cliente=cliente,
            medicion=medicion,
            fecha_vencimiento=timezone.now().date() + timezone.timedelta(days=30),
            monto_total=medicion.consumo_m3 * 500
        )
        print(f"✅ Boleta creada: #{boleta.numero_boleta}")
        
        # Crear un aviso
        aviso = Aviso.objects.create(
            cliente=cliente,
            tipo_aviso='corte_programado',
            titulo='Corte de Agua Programado',
            mensaje='Se informa que habrá corte de agua el día 15 de octubre de 8:00 a 12:00 horas.'
        )
        print(f"✅ Aviso creado: {aviso.titulo}")
        
        print("✅ Datos básicos creados exitosamente")
        
    except Exception as e:
        print(f"❌ Error creando datos: {e}")

def show_stats():
    """Mostrar estadísticas de la base de datos."""
    print("\n📊 Estadísticas de la base de datos:")
    print(f"👥 Clientes: {Cliente.objects.count()}")
    print(f"📊 Mediciones: {Medicion.objects.count()}")
    print(f"🧾 Boletas: {Boleta.objects.count()}")
    print(f"📢 Avisos: {Aviso.objects.count()}")

def main():
    """Función principal."""
    print("🗄️  Creación de Datos de Muestra")
    
    create_basic_data()
    show_stats()
    
    print("\n✅ Proceso completado!")
    print("🌐 Puedes acceder al sistema en: http://127.0.0.1:8000/")

if __name__ == "__main__":
    main()
