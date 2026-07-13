from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Producto(models.Model):
    CLASIFICACION_CHOICES = [
        ('SIM_AVANZADA', 'Simulación Avanzada'),
        ('AUDIO_INMERSIVO', 'Audio Inmersivo'),
        ('MOBILIARIO_PRO', 'Mobiliario Pro'),
    ]

    nombre = models.CharField(max_length=255, verbose_name="Nombre del Componente")
    clasificacion = models.CharField(max_length=50, choices=CLASIFICACION_CHOICES, default='SIM_AVANZADA', verbose_name="SKU / Clasificación")
    costo_comercial = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo Comercial ($ MXN)")
    especificaciones_tecnicas = models.TextField(blank=True, null=True, verbose_name="Especificaciones Técnicas")
    existencia_inicial = models.PositiveIntegerField(default=0, verbose_name="Existencia Inicial Almacén")
    
    # Campo de imagen adaptado exactamente del modelo Alumnos
    imagen = models.ImageField(null=True, upload_to="fotos", verbose_name="Fotografía")
    
    # Fechas corregidas al estándar de tu otro proyecto
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['-created']

    def __str__(self):
        # CORREGIDO: Se agregó la 'f' al inicio para evitar el error de sintaxis
        return f"{self.nombre} ({self.get_clasificacion_display()})"


class Orden(models.Model):
    METODOS_PAGO = [
        ('TARJETA', 'Tarjeta de Crédito / Débito'),
        ('PAYPAL', 'PayPal System'),
    ]
    
    nombre_completo = models.CharField(max_length=255, verbose_name="Nombre Completo")
    direccion_postal = models.CharField(max_length=255, verbose_name="Dirección Postal")
    estado_ciudad = models.CharField(max_length=150, verbose_name="Estado / Ciudad")
    codigo_postal = models.CharField(max_length=10, verbose_name="Código Postal")
    metodo_pago = models.CharField(max_length=20, choices=METODOS_PAGO, default='TARJETA')
    total_neto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Neto a Pagar")
    created = models.DateTimeField(auto_now_add=True) 

    class Meta:
        verbose_name = "Orden"
        verbose_name_plural = "Ordenes"
        ordering = ['-created']

    def __str__(self):
        return f"Orden #{self.id} - {self.nombre_completo}"


class OrdenItem(models.Model):
    """ Almacena los productos específicos de cada orden """
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre} en Orden #{self.orden.id}"

class Opinión(models.Model):
    STATUS_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('APROBADO', 'Aprobado'),
        ('RECHAZADO', 'Rechazado'),
    ]
    user = models.CharField(max_length=150, verbose_name="Usuario")
    message = models.TextField(verbose_name="Mensaje")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='APROBADO')
    response = models.TextField(blank=True, null=True, verbose_name="Respuesta")
    is_hidden = models.BooleanField(default=False)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        verbose_name = 'Opinión'
        verbose_name_plural = 'Opiniones'

    def __str__(self):
        return f"{self.user}: {self.message[:40]}"
    
class Usuario(models.Model):
    username = models.CharField(max_length=150, unique=True, verbose_name="Nombre de Usuario")
    email = models.EmailField(unique=True, verbose_name="Correo")
    password = models.CharField(max_length=255, verbose_name="Contraseña")
    is_admin = models.BooleanField(default=False, verbose_name="Es Administrador")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username