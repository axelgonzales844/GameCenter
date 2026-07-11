import stat

from django.contrib import admin
from django.urls import path
# Importamos las vistas de tu aplicación 'game'
from game import views
from game_center import settings
from settings import STATIC_URL 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.catalogo, name='catalogo'),
    path('altaproducto/', views.altaproducto, name='altaproducto'),
    path('opiniones/', views.opiniones, name='opiniones'),
]

if settings.DEBUG:
    from django.conf.urls.static import static 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)