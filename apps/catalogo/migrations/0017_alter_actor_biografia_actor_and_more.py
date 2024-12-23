# Generated by Django 5.1.1 on 2024-11-20 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0016_alter_actor_url_image_actor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actor',
            name='biografia_Actor',
            field=models.TextField(blank=True, default='Aún no se ha registrado una biografía.', null=True, verbose_name='Biografia'),
        ),
        migrations.AlterField(
            model_name='actor',
            name='correo_privado_actor',
            field=models.CharField(blank=True, default='...', max_length=100, null=True, verbose_name='Correo Privado'),
        ),
        migrations.AlterField(
            model_name='actor',
            name='correo_publico_Actor',
            field=models.CharField(blank=True, default='....', max_length=100, verbose_name='Correo Publico'),
        ),
    ]
