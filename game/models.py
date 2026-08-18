from decimal import Decimal

from django.db import models
from django.utils import timezone

# Create your models here.

class Usuario(models.Model):
    username = models.CharField(max_length=150, unique=True, verbose_name="Nombre de Usuario")
    email = models.EmailField(unique=True, verbose_name="Correo")
    password = models.CharField(max_length=255, verbose_name="Contraseña")
    is_admin = models.BooleanField(default=False, verbose_name="Es Administrador")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Producto(models.Model):
    CLASIFICACION_CHOICES = [
        ('SIM_AVANZADA', 'Simulación Avanzada'),
        ('AUDIO_INMERSIVO', 'Audio Inmersivo'),
        ('MOBILIARIO_PRO', 'Mobiliario Pro'),
    ]

    nombre = models.CharField(max_length=255, verbose_name="Nombre del Componente")
    clasificacion = models.CharField(max_length=50, choices=CLASIFICACION_CHOICES, default='SIM_AVANZADA', verbose_name="SKU / Clasificación")
    costo_comercial = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo Comercial ($ MXN)")
    descuento = models.PositiveIntegerField(default=0, verbose_name="Descuento (%)")
    descuento_inicio = models.DateTimeField(blank=True, null=True, verbose_name="Inicio del descuento")
    descuento_fin = models.DateTimeField(blank=True, null=True, verbose_name="Fin del descuento")
    descuento_minimo_unidades = models.PositiveIntegerField(default=0, verbose_name="Stock mínimo para descuento")
    especificaciones_tecnicas = models.TextField(blank=True, null=True, verbose_name="Especificaciones Técnicas")
    existencia_inicial = models.PositiveIntegerField(default=0, verbose_name="Existencia Inicial Almacén")
    
    imagen = models.ImageField(null=True, upload_to="fotos", verbose_name="Fotografía")
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)  # Se cambió a auto_now para actualización real

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['-created']

    def precio_con_descuento(self):
        if self.descuento <= 0:
            return self.costo_comercial

        ahora = timezone.now()
        if self.descuento_inicio and ahora < self.descuento_inicio:
            return self.costo_comercial
        if self.descuento_fin and ahora > self.descuento_fin:
            return self.costo_comercial
        if self.descuento_minimo_unidades and self.existencia_inicial < self.descuento_minimo_unidades:
            return self.costo_comercial

        descuento_decimal = Decimal(self.descuento) / Decimal('100')
        return self.costo_comercial * (Decimal('1') - descuento_decimal)

    def __str__(self):
        return f"{self.nombre} ({self.get_clasificacion_display()})"


class Orden(models.Model):
    METODOS_PAGO = [
        ('TARJETA', 'Tarjeta de Crédito / Débito'),
        ('PAYPAL', 'PayPal System'),
    ]
    
    # 🔗 NUEVO CAMPO: Conexión clave con tu modelo Usuario custom
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True, related_name='ordenes', verbose_name="Usuario")
    
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
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        verbose_name = 'Opinión'
        verbose_name_plural = 'Opiniones'

    def __str__(self):
        return f"{self.user}: {self.message[:40]}"

class Direccion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='direcciones', verbose_name="Usuario")
    calle = models.CharField(max_length=255, verbose_name="Calle")
    numero_exterior = models.CharField(max_length=20, verbose_name="Número Exterior")
    numero_interior = models.CharField(max_length=20, blank=True, null=True, verbose_name="Número Interior")
    colonia = models.CharField(max_length=150, verbose_name="Colonia / Fraccionamiento")
    codigo_postal = models.CharField(max_length=10, verbose_name="Código Postal")
    ciudad = models.CharField(max_length=150, verbose_name="Ciudad / Municipio")
    pais = models.CharField(max_length=100, default="México", verbose_name="País")
    numero_telefonico = models.CharField(max_length=20, verbose_name="Número Telefónico")
    referencias = models.TextField(blank=True, null=True, verbose_name="Referencias")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Dirección"
        verbose_name_plural = "Direcciones"
        ordering = ['-created']

    def __str__(self):
        return f"{self.calle} #{self.numero_exterior}, {self.colonia} ({self.usuario.username})"

class Carrito(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='carrito')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrito de {self.usuario.username}"


class ElementoCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='elementos')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"