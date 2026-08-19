from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from game import views
from game_center import settings

urlpatterns = [
    # Panel nativo de Django
    path('admin/', admin.site.urls),
    
    # Navegación Principal y Productos
    path('', views.catalogo, name='catalogo'),
    path('detallesproducto/<int:producto_id>/', views.detallesproducto, name='detallesproducto'),
    path('opiniones/', views.opiniones, name='opiniones'),
    
    # Carrito de Compras
    path('carrito/', views.carrito, name='carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/modificar/<int:producto_id>/<str:accion>/', views.cambiar_cantidad_carrito, name='cambiar_cantidad_carrito'),
    path('procesar-pago/', views.procesar_pago, name='procesar_pago'),
    
    # Autenticación y Cliente
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro, name='registro'),
    path('logout/', views.logout_view, name='logout'), 
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/agregar-direccion/', views.agregar_direccion, name='agregar_direccion'),
    
    # Administración Custom (Protegida por @admin_required)
    path('altaproducto/', views.altaproducto, name='altaproducto'),
    path('control/', views.control, name='control'),
    path('editar-producto/<int:id>/', views.editar_producto, name='editar_producto'),
    path('eliminar-producto/<int:id>/', views.eliminar_producto, name='eliminar_producto'),  # <-- RUTA AGREGADA
    path('admin-usuarios/', views.lista_usuarios, name='lista_usuarios'),
    # Administración de Opiniones
    path('admin-opiniones/', views.admin_opiniones, name='admin_opiniones'),
    path('eliminar-opinion/<int:id>/', views.eliminar_opinion, name='eliminar_opinion'),
    # Estadísticas y Pedidos Admin
    path('admin-estadisticas/', views.admin_estadisticas, name='admin_estadisticas'),
    path('admin-pedidos/', views.admin_pedidos, name='admin_pedidos'),
    path('sobre-nosotros/', views.sobre_nosotros, name='sobre_nosotros'),
    path('contacto/', views.contacto, name='contacto'),
    ]


# Configuración para servir archivos multimedia (imágenes de productos) en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)