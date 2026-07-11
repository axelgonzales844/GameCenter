import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'game_center.settings')
django.setup()

from game.models import Producto

# Limpiar datos existentes
Producto.objects.all().delete()

# Crear productos de prueba
productos = [
    {
        'nombre': 'Butaca Ergonómica Titan',
        'clasificacion': 'MOBILIARIO_PRO',
        'costo_comercial': 5499.00,
        'especificaciones_tecnicas': 'Material: Cuero sintético premium. Altura ajustable. Soporte lumbar ergonómico.',
        'existencia_inicial': 12,
    },
    {
        'nombre': 'Mando Elite Series Phantom',
        'clasificacion': 'CONTROLES_MANDOS',
        'costo_comercial': 2899.00,
        'especificaciones_tecnicas': 'Conectividad: Inalámbrica 2.4GHz. Batería: 40 horas. Vibración haptica.',
        'existencia_inicial': 2,
    },
    {
        'nombre': 'Kraken V3 HyperSense',
        'clasificacion': 'AUDIO_INMERSIVO',
        'costo_comercial': 3199.00,
        'especificaciones_tecnicas': 'Sonido 7.1 surround. Micrófono con cancelación de ruido. RGB personalizable.',
        'existencia_inicial': 8,
    },
    {
        'nombre': 'Render Titan Pro',
        'clasificacion': 'SIM_AVANZADA',
        'costo_comercial': 7999.00,
        'especificaciones_tecnicas': 'GPU RTX 4090. RAM 64GB. Almacenamiento NVMe 2TB.',
        'existencia_inicial': 5,
    },
    {
        'nombre': 'Render Elite Controller',
        'clasificacion': 'CONTROLES_MANDOS',
        'costo_comercial': 1499.00,
        'especificaciones_tecnicas': 'Botones programables. Sensibilidad ajustable. Compatible con PC y consolas.',
        'existencia_inicial': 15,
    },
    {
        'nombre': 'Audio Inmersivo Pro X',
        'clasificacion': 'AUDIO_INMERSIVO',
        'costo_comercial': 4299.00,
        'especificaciones_tecnicas': 'Dolby Atmos. Drivers de 50mm. Conectividad Bluetooth 5.3.',
        'existencia_inicial': 7,
    },
]

for prod in productos:
    Producto.objects.create(**prod)

print("Datos de prueba creados correctamente")
print(f"Total de productos: {Producto.objects.count()}")
