from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from io import BytesIO
import os

from .models import Cliente, Medicion, Boleta, Aviso
from .forms import ClienteForm, MedicionForm, BoletaForm, AvisoForm


def home(request):
    """Página principal del sistema"""
    context = {
        'total_clientes': Cliente.objects.filter(activo=True).count(),
        'boletas_pendientes': Boleta.objects.filter(estado='pendiente').count(),
        'aviso_pendientes': Aviso.objects.filter(enviado=False).count(),
        'ultimas_mediciones': Medicion.objects.select_related('cliente').order_by('-fecha')[:5],
    }
    return render(request, 'facturacion/home.html', context)


def lista_clientes(request):
    """Lista todos los clientes"""
    clientes = Cliente.objects.all().order_by('nombre')
    return render(request, 'facturacion/lista_clientes.html', {'clientes': clientes})


def crear_cliente(request):
    """Crear nuevo cliente"""
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente creado exitosamente.')
            return redirect('lista_clientes')
    else:
        form = ClienteForm()
    
    return render(request, 'facturacion/crear_cliente.html', {'form': form})


def detalle_cliente(request, cliente_id):
    """Detalle de un cliente específico"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    mediciones = Medicion.objects.filter(cliente=cliente).order_by('-fecha')[:10]
    boletas = Boleta.objects.filter(cliente=cliente).order_by('-fecha_emision')[:10]
    avisos = Aviso.objects.filter(cliente=cliente).order_by('-fecha')[:5]
    
    context = {
        'cliente': cliente,
        'mediciones': mediciones,
        'boletas': boletas,
        'avisos': avisos,
    }
    return render(request, 'facturacion/detalle_cliente.html', context)


def crear_medicion(request):
    """Crear nueva medición"""
    if request.method == 'POST':
        form = MedicionForm(request.POST)
        if form.is_valid():
            medicion = form.save()
            messages.success(request, f'Medición registrada. Consumo: {medicion.consumo_m3} m³')
            return redirect('detalle_cliente', cliente_id=medicion.cliente.id)
    else:
        form = MedicionForm()
    
    return render(request, 'facturacion/crear_medicion.html', {'form': form})


def generar_boleta(request):
    """Generar nueva boleta"""
    if request.method == 'POST':
        form = BoletaForm(request.POST)
        if form.is_valid():
            boleta = form.save(commit=False)
            boleta.monto_total = boleta.medicion.monto_calculado
            boleta.save()
            messages.success(request, f'Boleta #{boleta.numero_boleta} generada exitosamente.')
            return redirect('detalle_cliente', cliente_id=boleta.cliente.id)
    else:
        form = BoletaForm()
    
    return render(request, 'facturacion/generar_boleta.html', {'form': form})


def generar_pdf_boleta(request, boleta_id):
    """Generar PDF de boleta"""
    boleta = get_object_or_404(Boleta, id=boleta_id)
    
    # Crear buffer para el PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1,  # Centrado
    )
    
    # Título
    story.append(Paragraph("PRUEBA", title_style))
    story.append(Paragraph("Sistema de Facturación", styles['Heading2']))
    story.append(Spacer(1, 20))
    
    # Información de la boleta
    boleta_data = [
        ['Número de Boleta:', boleta.numero_boleta],
        ['Fecha de Emisión:', boleta.fecha_emision.strftime('%d/%m/%Y')],
        ['Fecha de Vencimiento:', boleta.fecha_vencimiento.strftime('%d/%m/%Y')],
        ['Estado:', boleta.get_estado_display()],
    ]
    
    boleta_table = Table(boleta_data, colWidths=[2*inch, 3*inch])
    boleta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (1, 0), (1, -1), colors.beige),
    ]))
    
    story.append(boleta_table)
    story.append(Spacer(1, 20))
    
    # Información del cliente
    story.append(Paragraph("DATOS DEL CLIENTE", styles['Heading2']))
    cliente_data = [
        ['Nombre:', boleta.cliente.nombre],
        ['Dirección:', boleta.cliente.direccion],
        ['Email:', boleta.cliente.email],
        ['Teléfono:', boleta.cliente.telefono or 'No registrado'],
    ]
    
    cliente_table = Table(cliente_data, colWidths=[2*inch, 3*inch])
    cliente_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (1, 0), (1, -1), colors.beige),
    ]))
    
    story.append(cliente_table)
    story.append(Spacer(1, 20))
    
    # Detalles de la medición
    story.append(Paragraph("DETALLES DE CONSUMO", styles['Heading2']))
    medicion_data = [
        ['Fecha de Medición:', boleta.medicion.fecha.strftime('%d/%m/%Y')],
        ['Consumo (m³):', f"{boleta.medicion.consumo_m3} m³"],
        ['Tarifa por m³:', '$500 CLP'],
        ['Monto Total:', f"${boleta.monto_total:,.2f} CLP"],
    ]
    
    medicion_table = Table(medicion_data, colWidths=[2*inch, 3*inch])
    medicion_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (1, 0), (1, -1), colors.beige),
        ('FONTNAME', (3, 3), (3, 3), 'Helvetica-Bold'),
        ('FONTSIZE', (3, 3), (3, 3), 12),
    ]))
    
    story.append(medicion_table)
    story.append(Spacer(1, 30))
    
    # Pie de página
    story.append(Paragraph("Gracias por su preferencia", styles['Normal']))
    story.append(Paragraph("Prueba - Sistema de Facturación", styles['Normal']))
    
    # Construir PDF
    doc.build(story)
    buffer.seek(0)
    
    # Respuesta HTTP
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="boleta_{boleta.numero_boleta}.pdf"'
    return response


def enviar_boleta_email(request, boleta_id):
    """Enviar boleta por correo electrónico"""
    boleta = get_object_or_404(Boleta, id=boleta_id)
    
    try:
        # Generar PDF
        buffer = BytesIO()
        # ... (código de generación de PDF similar al anterior)
        
        # Enviar email
        subject = f'Boleta de Agua - {boleta.numero_boleta}'
        message = f'''
        Estimado/a {boleta.cliente.nombre},
        
        Adjunto encontrará su boleta de agua correspondiente al período.
        
        Detalles:
        - Número de Boleta: {boleta.numero_boleta}
        - Fecha de Emisión: {boleta.fecha_emision}
        - Fecha de Vencimiento: {boleta.fecha_vencimiento}
        - Monto: ${boleta.monto_total:,.2f} CLP
        
        Gracias por su preferencia.
        
        Prueba
        '''
        
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [boleta.cliente.email],
            fail_silently=False,
        )
        
        messages.success(request, f'Boleta enviada exitosamente a {boleta.cliente.email}')
        
    except Exception as e:
        messages.error(request, f'Error al enviar el correo: {str(e)}')
    
    return redirect('detalle_cliente', cliente_id=boleta.cliente.id)


def crear_aviso(request):
    """Crear nuevo aviso"""
    if request.method == 'POST':
        form = AvisoForm(request.POST)
        if form.is_valid():
            aviso = form.save()
            messages.success(request, 'Aviso creado exitosamente.')
            return redirect('detalle_cliente', cliente_id=aviso.cliente.id)
    else:
        form = AvisoForm()
    
    return render(request, 'facturacion/crear_aviso.html', {'form': form})


def enviar_aviso_email(request, aviso_id):
    """Enviar aviso por correo electrónico"""
    aviso = get_object_or_404(Aviso, id=aviso_id)
    
    try:
        subject = f'{aviso.titulo} - Prueba'
        message = f'''
        Estimado/a {aviso.cliente.nombre},
        
        {aviso.mensaje}
        
        Tipo de Aviso: {aviso.get_tipo_aviso_display()}
        Fecha: {aviso.fecha.strftime('%d/%m/%Y %H:%M')}
        
        Gracias por su atención.
        
        Prueba
        '''
        
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [aviso.cliente.email],
            fail_silently=False,
        )
        
        # Marcar como enviado
        aviso.enviado = True
        aviso.fecha_envio = timezone.now()
        aviso.save()
        
        messages.success(request, f'Aviso enviado exitosamente a {aviso.cliente.email}')
        
    except Exception as e:
        messages.error(request, f'Error al enviar el aviso: {str(e)}')
    
    return redirect('detalle_cliente', cliente_id=aviso.cliente.id)


def lista_boletas(request):
    """Lista todas las boletas"""
    boletas = Boleta.objects.select_related('cliente').order_by('-fecha_emision')
    return render(request, 'facturacion/lista_boletas.html', {'boletas': boletas})


def lista_avisos(request):
    """Lista todos los avisos"""
    avisos = Aviso.objects.select_related('cliente').order_by('-fecha')
    return render(request, 'facturacion/lista_avisos.html', {'avisos': avisos})


# ===== NUEVAS VISTAS PARA GESTIÓN COMPLETA =====

def editar_cliente(request, cliente_id):
    """Editar información de un cliente"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, f'Cliente {cliente.nombre} actualizado exitosamente.')
            return redirect('detalle_cliente', cliente_id=cliente.id)
    else:
        form = ClienteForm(instance=cliente)
    
    return render(request, 'facturacion/editar_cliente.html', {'form': form, 'cliente': cliente})


def eliminar_cliente(request, cliente_id):
    """Eliminar un cliente"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        nombre = cliente.nombre
        cliente.delete()
        messages.success(request, f'Cliente {nombre} eliminado exitosamente.')
        return redirect('lista_clientes')
    
    return render(request, 'facturacion/eliminar_cliente.html', {'cliente': cliente})


def toggle_cliente_activo(request, cliente_id):
    """Activar/Desactivar cliente"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    cliente.activo = not cliente.activo
    cliente.save()
    
    estado = "activado" if cliente.activo else "desactivado"
    messages.success(request, f'Cliente {cliente.nombre} {estado} exitosamente.')
    return redirect('detalle_cliente', cliente_id=cliente.id)


def lista_mediciones(request):
    """Lista todas las mediciones"""
    mediciones = Medicion.objects.select_related('cliente').order_by('-fecha')
    return render(request, 'facturacion/lista_mediciones.html', {'mediciones': mediciones})


def editar_medicion(request, medicion_id):
    """Editar una medición"""
    medicion = get_object_or_404(Medicion, id=medicion_id)
    if request.method == 'POST':
        form = MedicionForm(request.POST, instance=medicion)
        if form.is_valid():
            form.save()
            messages.success(request, f'Medición actualizada exitosamente.')
            return redirect('detalle_cliente', cliente_id=medicion.cliente.id)
    else:
        form = MedicionForm(instance=medicion)
    
    return render(request, 'facturacion/editar_medicion.html', {'form': form, 'medicion': medicion})


def eliminar_medicion(request, medicion_id):
    """Eliminar una medición"""
    medicion = get_object_or_404(Medicion, id=medicion_id)
    cliente_id = medicion.cliente.id
    if request.method == 'POST':
        medicion.delete()
        messages.success(request, 'Medición eliminada exitosamente.')
        return redirect('detalle_cliente', cliente_id=cliente_id)
    
    return render(request, 'facturacion/eliminar_medicion.html', {'medicion': medicion})


def cambiar_estado_boleta(request, boleta_id):
    """Cambiar estado de una boleta"""
    boleta = get_object_or_404(Boleta, id=boleta_id)
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado in ['pendiente', 'pagada', 'vencida', 'cancelada']:
            boleta.estado = nuevo_estado
            boleta.save()
            messages.success(request, f'Estado de boleta #{boleta.numero_boleta} cambiado a {boleta.get_estado_display()}.')
        return redirect('detalle_cliente', cliente_id=boleta.cliente.id)
    
    return render(request, 'facturacion/cambiar_estado_boleta.html', {'boleta': boleta})


def eliminar_boleta(request, boleta_id):
    """Eliminar una boleta"""
    boleta = get_object_or_404(Boleta, id=boleta_id)
    cliente_id = boleta.cliente.id
    if request.method == 'POST':
        numero = boleta.numero_boleta
        boleta.delete()
        messages.success(request, f'Boleta #{numero} eliminada exitosamente.')
        return redirect('detalle_cliente', cliente_id=cliente_id)
    
    return render(request, 'facturacion/eliminar_boleta.html', {'boleta': boleta})


def editar_aviso(request, aviso_id):
    """Editar un aviso"""
    aviso = get_object_or_404(Aviso, id=aviso_id)
    if request.method == 'POST':
        form = AvisoForm(request.POST, instance=aviso)
        if form.is_valid():
            form.save()
            messages.success(request, f'Aviso actualizado exitosamente.')
            return redirect('detalle_cliente', cliente_id=aviso.cliente.id)
    else:
        form = AvisoForm(instance=aviso)
    
    return render(request, 'facturacion/editar_aviso.html', {'form': form, 'aviso': aviso})


def eliminar_aviso(request, aviso_id):
    """Eliminar un aviso"""
    aviso = get_object_or_404(Aviso, id=aviso_id)
    cliente_id = aviso.cliente.id
    if request.method == 'POST':
        aviso.delete()
        messages.success(request, 'Aviso eliminado exitosamente.')
        return redirect('detalle_cliente', cliente_id=cliente_id)
    
    return render(request, 'facturacion/eliminar_aviso.html', {'aviso': aviso})


def buscar(request):
    """Búsqueda global en el sistema"""
    query = request.GET.get('q', '')
    resultados = {
        'clientes': [],
        'boletas': [],
        'avisos': []
    }
    
    if query:
        resultados['clientes'] = Cliente.objects.filter(
            nombre__icontains=query
        ).order_by('nombre')[:10]
        
        resultados['boletas'] = Boleta.objects.filter(
            numero_boleta__icontains=query
        ).select_related('cliente').order_by('-fecha_emision')[:10]
        
        resultados['avisos'] = Aviso.objects.filter(
            titulo__icontains=query
        ).select_related('cliente').order_by('-fecha')[:10]
    
    return render(request, 'facturacion/buscar.html', {
        'query': query,
        'resultados': resultados
    })


def reportes(request):
    """Página de reportes y estadísticas"""
    from django.db.models import Sum, Count, Avg
    from datetime import datetime, timedelta
    
    # Estadísticas generales
    stats = {
        'total_clientes': Cliente.objects.filter(activo=True).count(),
        'total_boletas': Boleta.objects.count(),
        'boletas_pendientes': Boleta.objects.filter(estado='pendiente').count(),
        'boletas_pagadas': Boleta.objects.filter(estado='pagada').count(),
        'boletas_vencidas': Boleta.objects.filter(estado='vencida').count(),
        'ingresos_totales': Boleta.objects.filter(estado='pagada').aggregate(
            total=Sum('monto_total')
        )['total'] or 0,
        'consumo_promedio': Medicion.objects.aggregate(
            promedio=Avg('consumo_m3')
        )['promedio'] or 0,
    }
    
    # Boletas por mes (últimos 6 meses)
    from django.utils import timezone
    seis_meses_atras = timezone.now() - timedelta(days=180)
    boletas_por_mes = Boleta.objects.filter(
        fecha_emision__gte=seis_meses_atras
    ).extra(
        select={'mes': "strftime('%%Y-%%m', fecha_emision)"}
    ).values('mes').annotate(
        cantidad=Count('id'),
        total=Sum('monto_total')
    ).order_by('mes')
    
    return render(request, 'facturacion/reportes.html', {
        'stats': stats,
        'boletas_por_mes': boletas_por_mes
    })
