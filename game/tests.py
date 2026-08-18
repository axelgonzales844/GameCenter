from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Producto


class CatalogoSearchTests(TestCase):
    def setUp(self):
        ahora = timezone.now()
        Producto.objects.create(
            nombre='Teclado Gamer RGB',
            clasificacion='SIM_AVANZADA',
            costo_comercial=1500,
            especificaciones_tecnicas='Teclado mecánico con switches rojos.',
            existencia_inicial=10,
            descuento=15,
            descuento_inicio=ahora - timedelta(days=1),
            descuento_fin=ahora + timedelta(days=3),
            descuento_minimo_unidades=5,
        )
        Producto.objects.create(
            nombre='Monitor 4K',
            clasificacion='AUDIO_INMERSIVO',
            costo_comercial=2500,
            especificaciones_tecnicas='Monitor de 27 pulgadas ultra HD.',
            existencia_inicial=5,
            descuento=0,
        )

    def test_catalogo_filtra_por_termino_de_busqueda(self):
        response = self.client.get(reverse('catalogo'), {'q': 'teclado'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Teclado Gamer RGB')
        self.assertNotContains(response, 'Monitor 4K')

    def test_producto_puede_guardar_y_mostrar_descuento_activo(self):
        producto = Producto.objects.get(nombre='Teclado Gamer RGB')

        self.assertEqual(producto.descuento, 15)
        self.assertEqual(producto.precio_con_descuento(), 1275)
        self.assertContains(self.client.get(reverse('catalogo')), '15%')

    def test_descuento_no_aplica_si_fuera_de_vigencia_o_stock(self):
        producto = Producto.objects.get(nombre='Teclado Gamer RGB')
        producto.descuento_fin = timezone.now() - timedelta(minutes=5)
        producto.save()

        self.assertEqual(producto.precio_con_descuento(), producto.costo_comercial)

        producto.descuento_fin = timezone.now() + timedelta(days=3)
        producto.existencia_inicial = 2
        producto.save()

        self.assertEqual(producto.precio_con_descuento(), producto.costo_comercial)
