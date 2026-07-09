from django.contrib import admin
from django.urls import path
# Importamos las vistas de tu aplicación 'game'
from game import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.catalogo, name='catalogo'),
]