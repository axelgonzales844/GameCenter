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

class Orden(models.Model):
    METODOS_PAGO = [('TARJETA', 'Tarjeta de Crédito / Débito'),('PAYPAL', 'PayPal System'),]
    # Relación opcional con un usuario registrado
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    # --- 1. Destino de Entrega ---
    nombre_completo = models.CharField(max_length=255, verbose_name="Nombre Completo")
    direccion_postal = models.CharField(max_length=255, verbose_name="Dirección Postal")
    estado_ciudad = models.CharField(max_length=150, verbose_name="Estado / Ciudad")
    codigo_postal = models.CharField(max_length=10, verbose_name="Código Postal")
    
    # --- 2. Método de Pago ---
    metodo_pago = models.CharField(max_length=20, choices=METODOS_PAGO, default='TARJETA')
    # Nota de seguridad: NUNCA guardes el número de tarjeta completo, CVV o expiración en tu base de datos local.
    # Eso lo gestiona de forma segura un procesador de pagos (Stripe, PayPal SDK, etc.).
    
    # --- Revisión de Orden ---
    total_neto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Neto a Pagar")
    creado_el = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Orden"
        verbose_name_plural = "Ordenes"
        ordering = ['-creado_el']

    def __str__(self):
        return f"Orden #{self.id} - {self.nombre_completo}"


class OrdenItem(models.Model):
    """ Almacena los productos específicos de cada orden """
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2) # Precio histórico de compra

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre} en Orden #{self.orden.id}"