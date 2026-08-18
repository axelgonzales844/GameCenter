from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0010_carrito_elementocarrito'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='descuento',
            field=models.PositiveIntegerField(default=0, verbose_name='Descuento (%)'),
        ),
        migrations.AddField(
            model_name='producto',
            name='descuento_fin',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Fin del descuento'),
        ),
        migrations.AddField(
            model_name='producto',
            name='descuento_inicio',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Inicio del descuento'),
        ),
        migrations.AddField(
            model_name='producto',
            name='descuento_minimo_unidades',
            field=models.PositiveIntegerField(default=0, verbose_name='Stock mínimo para descuento'),
        ),
    ]
