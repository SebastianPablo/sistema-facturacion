from django.urls import path
from . import views

urlpatterns = [
    # Página principal
    path('', views.home, name='home'),
    
    # Gestión de clientes
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/crear/', views.crear_cliente, name='crear_cliente'),
    path('clientes/<int:cliente_id>/', views.detalle_cliente, name='detalle_cliente'),
    path('clientes/<int:cliente_id>/editar/', views.editar_cliente, name='editar_cliente'),
    path('clientes/<int:cliente_id>/eliminar/', views.eliminar_cliente, name='eliminar_cliente'),
    path('clientes/<int:cliente_id>/toggle-activo/', views.toggle_cliente_activo, name='toggle_cliente_activo'),
    
    # Gestión de mediciones
    path('mediciones/', views.lista_mediciones, name='lista_mediciones'),
    path('mediciones/crear/', views.crear_medicion, name='crear_medicion'),
    path('mediciones/<int:medicion_id>/editar/', views.editar_medicion, name='editar_medicion'),
    path('mediciones/<int:medicion_id>/eliminar/', views.eliminar_medicion, name='eliminar_medicion'),
    
    # Gestión de boletas
    path('boletas/', views.lista_boletas, name='lista_boletas'),
    path('boletas/generar/', views.generar_boleta, name='generar_boleta'),
    path('boletas/<int:boleta_id>/pdf/', views.generar_pdf_boleta, name='generar_pdf_boleta'),
    path('boletas/<int:boleta_id>/enviar/', views.enviar_boleta_email, name='enviar_boleta_email'),
    path('boletas/<int:boleta_id>/cambiar-estado/', views.cambiar_estado_boleta, name='cambiar_estado_boleta'),
    path('boletas/<int:boleta_id>/eliminar/', views.eliminar_boleta, name='eliminar_boleta'),
    
    # Gestión de avisos
    path('avisos/', views.lista_avisos, name='lista_avisos'),
    path('avisos/crear/', views.crear_aviso, name='crear_aviso'),
    path('avisos/<int:aviso_id>/editar/', views.editar_aviso, name='editar_aviso'),
    path('avisos/<int:aviso_id>/eliminar/', views.eliminar_aviso, name='eliminar_aviso'),
    path('avisos/<int:aviso_id>/enviar/', views.enviar_aviso_email, name='enviar_aviso_email'),
    
    # Búsqueda y reportes
    path('buscar/', views.buscar, name='buscar'),
    path('reportes/', views.reportes, name='reportes'),
]
