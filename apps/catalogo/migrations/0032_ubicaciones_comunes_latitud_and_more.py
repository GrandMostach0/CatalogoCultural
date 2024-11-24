# Generated by Django 5.1.1 on 2024-11-24 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0031_publicacioneventos_hora_inicio'),
    ]

    operations = [
        migrations.AddField(
            model_name='ubicaciones_comunes',
            name='latitud',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Latitud'),
        ),
        migrations.AddField(
            model_name='ubicaciones_comunes',
            name='longitud',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Longitud'),
        ),
    ]
