from django.contrib import admin
from .models import Producto, Opinión, Usuario, Duda, AlertaStock

admin.site.site_header = 'Game Center Admin'
admin.site.site_title = 'Game Center'
admin.site.index_title = 'Panel de control'


class ProductoModelo(admin.ModelAdmin):
    list_display = ('nombre', 'clasificacion', 'costo_comercial', 'existencia_inicial')
    list_filter = ('costo_comercial', 'clasificacion')
    search_fields = ('nombre', 'especificaciones_tecnicas')

    class Media:
        css = {
            'all': ('game/css/admin.css',)
        }


class OpiniónAdmin(admin.ModelAdmin):
    list_display = ('user', 'message_snippet', 'status', 'is_hidden', 'created')
    list_editable = ('status', 'is_hidden')  # Permite cambiar el estado directo en la lista sin entrar a editar
    list_filter = ('status', 'created', 'is_hidden')
    search_fields = ('user', 'message')
    readonly_fields = ('created', 'updated')
    actions = ['aprobar_opiniones', 'rechazar_opiniones']  # Acciones masivas

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

    def message_snippet(self, obj):
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message
    message_snippet.short_description = "Mensaje"

    @admin.action(description="Aprobar opiniones seleccionadas")
    def aprobar_opiniones(self, request, queryset):
        filas_actualizadas = queryset.update(status='APROBADO')
        self.message_user(request, f"{filas_actualizadas} opinión(es) aprobada(s) correctamente.")

    @admin.action(description="Rechazar opiniones seleccionadas")
    def rechazar_opiniones(self, request, queryset):
        filas_actualizadas = queryset.update(status='RECHAZADO')
        self.message_user(request, f"{filas_actualizadas} opinión(es) rechazada(s) correctamente.")

    class Media:
        css = {
            'all': ('game/css/admin.css',)
        }


class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_admin', 'created')
    list_filter = ('is_admin',)
    search_fields = ('username', 'email')
    readonly_fields = ('password', 'created')

    class Media:
        css = {
            'all': ('game/css/admin.css',)
        }

@admin.register(Duda)
class DudaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'created')

@admin.register(AlertaStock)
class AlertaStockAdmin(admin.ModelAdmin):
    list_display = ('email', 'producto', 'notificado', 'created')
    list_filter = ('notificado',)
    search_fields = ('email', 'producto__nombre')
    readonly_fields = ('created',)

# Registramos el modelo con su configuración
admin.site.register(Producto, ProductoModelo)
admin.site.register(Opinión, OpiniónAdmin)
admin.site.register(Usuario, UsuarioAdmin)
