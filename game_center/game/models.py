from django.db import models

# Create your models here.


class Producto(models.Model):
    # Opciones para el campo SKU / Clasificación
    CLASIFICACION_CHOICES = [
        ('SIM_AVANZADA', 'Simulación Avanzada'),
        ('AUDIO_INMERSIVO', 'Audio Inmersivo'),
        ('MOBILIARIO_PRO', 'Mobiliario Pro'),
    ]

    nombre = models.CharField(max_length=255, verbose_name="Nombre del Componente" )
    clasificacion = models.CharField(max_length=50,choices=CLASIFICACION_CHOICES,default='SIM_AVANZADA',verbose_name="SKU / Clasificación")
    costo_comercial = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo Comercial ($ MXN)")
    especificaciones_tecnicas = models.TextField(blank=True, null=True, verbose_name="Especificaciones Técnicas")
    existencia_inicial = models.PositiveIntegerField(default=0, verbose_name="Existencia Inicial Almacén")
    create = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['-create']

    def __str__(self):
        return f"{self.nombre} ({self.get_clasificacion_display()})"





class Opinión(models.Model):
    STATUS_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('APROBADO', 'Aprobado'),
        ('RECHAZADO', 'Rechazado'),
    ]

    user = models.CharField(max_length=150, verbose_name="Usuario")
    message = models.TextField(verbose_name="Mensaje")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDIENTE')
    response = models.TextField(blank=True, null=True, verbose_name="Respuesta")
    is_hidden = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        verbose_name = 'Opinión'
        verbose_name_plural = 'Opiniones'

    def __str__(self):
        return f"{self.user}: {self.message[:40]}"