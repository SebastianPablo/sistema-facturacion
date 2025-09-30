#!/usr/bin/env python
"""
Script para optimizar la base de datos.
"""

import os
import subprocess
import sys
from django.core.management import execute_from_command_line

def analyze_database():
    """Analizar rendimiento de la base de datos."""
    print("📊 Analizando rendimiento de la base de datos...")
    
    try:
        # Ejecutar análisis de Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aguas_del_valle.settings')
        
        # Importar Django
        import django
        django.setup()
        
        from django.db import connection
        from facturacion.models import Cliente, Medicion, Boleta, Aviso
        
        # Estadísticas de la base de datos
        print(f"👥 Clientes: {Cliente.objects.count()}")
        print(f"📊 Mediciones: {Medicion.objects.count()}")
        print(f"🧾 Boletas: {Boleta.objects.count()}")
        print(f"📢 Avisos: {Aviso.objects.count()}")
        
        # Análisis de consultas
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print(f"📋 Tablas: {len(tables)}")
            
            for table in tables:
                table_name = table[0]
                cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
                count = cursor.fetchone()[0]
                print(f"  📄 {table_name}: {count} registros")
        
        print("✅ Análisis completado")
        
    except Exception as e:
        print(f"❌ Error en análisis: {e}")

def create_sample_data():
    """Crear datos de muestra para testing."""
    print("🎭 Creando datos de muestra...")
    
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aguas_del_valle.settings')
        
        import django
        django.setup()
        
        from django.utils import timezone
        from facturacion.models import Cliente, Medicion, Boleta, Aviso
        from decimal import Decimal
        import random
        
        # Crear clientes de muestra
        clientes_data = [
            {
                'nombre': 'Juan Pérez',
                'email': 'juan.perez@email.com',
                'direccion': 'Av. Principal 123, Santiago',
                'telefono': '+56912345678'
            },
            {
                'nombre': 'María González',
                'email': 'maria.gonzalez@email.com',
                'direccion': 'Calle Secundaria 456, Valparaíso',
                'telefono': '+56987654321'
            },
            {
                'nombre': 'Carlos Silva',
                'email': 'carlos.silva@email.com',
                'direccion': 'Plaza Central 789, Concepción',
                'telefono': '+56911223344'
            }
        ]
        
        clientes = []
        for data in clientes_data:
            cliente, created = Cliente.objects.get_or_create(
                email=data['email'],
                defaults=data
            )
            clientes.append(cliente)
            if created:
                print(f"✅ Cliente creado: {cliente.nombre}")
        
        # Crear mediciones de muestra
        for cliente in clientes:
            for i in range(3):  # 3 mediciones por cliente
                fecha = timezone.now().date() - timezone.timedelta(days=30*i)
                consumo = Decimal(str(random.uniform(10, 50)))
                
                medicion = Medicion.objects.create(
                    cliente=cliente,
                    fecha=fecha,
                    consumo_m3=consumo,
                    lectura_anterior=Decimal(str(random.uniform(100, 200))),
                    lectura_actual=Decimal(str(random.uniform(200, 300))),
                    observaciones=f"Medición mensual {i+1}"
                )
                print(f"✅ Medición creada: {cliente.nombre} - {consumo} m³")
                
                # Crear boleta para la medición
                boleta = Boleta.objects.create(
                    cliente=cliente,
                    medicion=medicion,
                    fecha_vencimiento=fecha + timezone.timedelta(days=30),
                    monto_total=consumo * 500
                )
                print(f"✅ Boleta creada: #{boleta.numero_boleta}")
        
        # Crear avisos de muestra
        avisos_data = [
            {
                'tipo_aviso': 'corte_programado',
                'titulo': 'Corte de Agua Programado',
                'mensaje': 'Se informa que habrá corte de agua el día 15 de octubre de 8:00 a 12:00 horas.'
            },
            {
                'tipo_aviso': 'mantenimiento',
                'titulo': 'Mantenimiento de Red',
                'mensaje': 'Se realizará mantenimiento preventivo en la red de distribución.'
            }
        ]
        
        for aviso_data in avisos_data:
            for cliente in clientes:
                aviso = Aviso.objects.create(
                    cliente=cliente,
                    **aviso_data
                )
                print(f"✅ Aviso creado: {aviso.titulo} para {cliente.nombre}")
        
        print("✅ Datos de muestra creados exitosamente")
        
    except Exception as e:
        print(f"❌ Error creando datos de muestra: {e}")

def optimize_queries():
    """Optimizar consultas de la base de datos."""
    print("⚡ Optimizando consultas...")
    
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aguas_del_valle.settings')
        
        import django
        django.setup()
        
        from facturacion.models import Cliente, Medicion, Boleta, Aviso
        
        # Optimizar consultas con select_related y prefetch_related
        print("🔍 Optimizando consultas de clientes...")
        clientes_optimizados = Cliente.objects.select_related().prefetch_related(
            'medicion_set', 'boleta_set', 'aviso_set'
        ).filter(activo=True)
        
        print(f"✅ {clientes_optimizados.count()} clientes optimizados")
        
        # Optimizar consultas de mediciones
        print("🔍 Optimizando consultas de mediciones...")
        mediciones_optimizadas = Medicion.objects.select_related('cliente').order_by('-fecha')
        
        print(f"✅ {mediciones_optimizadas.count()} mediciones optimizadas")
        
        print("✅ Optimización completada")
        
    except Exception as e:
        print(f"❌ Error en optimización: {e}")

def main():
    """Función principal."""
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'analyze':
            analyze_database()
        elif command == 'sample':
            create_sample_data()
        elif command == 'optimize':
            optimize_queries()
        else:
            print("❌ Comando no válido")
    else:
        print("🗄️  Optimización de Base de Datos")
        print("\nComandos disponibles:")
        print("  python optimize_database.py analyze  - Analizar rendimiento")
        print("  python optimize_database.py sample    - Crear datos de muestra")
        print("  python optimize_database.py optimize  - Optimizar consultas")

if __name__ == "__main__":
    main()
