from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from game import views
from game_center import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.catalogo, name='catalogo'),
    path('altaproducto/', views.altaproducto, name='altaproducto'),
    path('opiniones/', views.opiniones, name='opiniones'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro, name='registro'),
    path('carrito/',views.carrito,name='carrito'),
    path('control/',views.control,name='control'),
    path('detallesproducto/<int:producto_id>/', views.detallesproducto, name='detallesproducto'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)