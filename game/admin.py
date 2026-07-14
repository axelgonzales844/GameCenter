from django.contrib import admin
from .models import Producto, Opinión, Usuario

class ProductoModelo(admin.ModelAdmin):
    list_display = ('nombre', 'clasificacion', 'costo_comercial', 'existencia_inicial')
    list_filter = ('costo_comercial', 'clasificacion') 
    search_fields = ('nombre', 'especificaciones_tecnicas')

class OpiniónAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'created', 'is_hidden')
    list_filter = ('status', 'created', 'is_hidden')
    search_fields = ('user', 'message')
    readonly_fields = ('created', 'updated') 
    
    fieldsets = (
        ('Información', {
            'fields': ('user', 'message')
        }),
        ('Moderación', {
            'fields': ('status', 'is_hidden')
        }),
        ('Timestamps', {
            'fields': ('created', 'updated'),
            'classes': ('collapse',)
        }),
    )
 
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_admin', 'created') 
    list_filter = ('is_admin',) 
    search_fields = ('username', 'email') 
    readonly_fields = ('password', 'created') 

# Registramos el modelo con su configuración
admin.site.register(Producto, ProductoModelo) 
admin.site.register(Opinión, OpiniónAdmin) 
admin.site.register(Usuario, UsuarioAdmin) 