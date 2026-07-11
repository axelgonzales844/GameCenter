from django.contrib import admin
from .models import Producto  # Corregido a singular

class ProductoModelo(admin.ModelAdmin):
    # Campos que se mostrarán en las columnas del panel de administración
    list_display = ('nombre', 'clasificacion', 'costo_comercial', 'existencia_inicial')
    
    # Filtro lateral (Cambiado 'precio' por 'costo_comercial')
    list_filter = ('costo_comercial', 'clasificacion')
    
    # Buscador por nombre o especificaciones
    search_fields = ('nombre', 'especificaciones_tecnicas')

# Registramos el modelo con su configuración corregida
admin.site.register(Producto, ProductoModelo)