# Generated by Django 5.1.1 on 2024-11-24 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0030_remove_publicacionobras_id_ubicacionescomunes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicacioneventos',
            name='hora_inicio',
            field=models.TimeField(blank=True, null=True, verbose_name='hora Inicio'),
        ),
    ]
