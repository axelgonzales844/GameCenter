from django.contrib import admin
from django.urls import path
# Importamos las vistas de tu aplicación 'game'
from game import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.altaproducto, name='altaproducto'),
    path('catalogo2/', views.catalogo2, name='catalogo2'),
    path('opiniones/', views.opiniones, name='opiniones'),
]