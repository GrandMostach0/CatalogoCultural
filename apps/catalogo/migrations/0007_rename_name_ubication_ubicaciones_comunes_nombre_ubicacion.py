# Generated by Django 5.1.1 on 2024-11-12 22:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0006_ubicaciones_comunes_name_ubication_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ubicaciones_comunes',
            old_name='name_ubication',
            new_name='nombre_ubicacion',
        ),
    ]
