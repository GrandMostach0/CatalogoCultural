# Generated by Django 5.1.1 on 2024-11-20 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0015_actor_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actor',
            name='url_image_actor',
            field=models.ImageField(blank=True, default='imagenes/default/imagenPerfil.jpg', null=True, upload_to='imagenes/', verbose_name='Image Perfil'),
        ),
    ]
