# Generated by Django 5.1.1 on 2024-11-23 20:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0022_alter_cat_redsocial_logo'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imagenes_publicaciones',
            name='id_publicacion',
        ),
        migrations.AddField(
            model_name='escuelas',
            name='tipo_escuela',
            field=models.BooleanField(default=False, verbose_name='Es público'),
        ),
        migrations.AddField(
            model_name='imagenes_publicaciones',
            name='content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='imagenes_publicaciones',
            name='object_id',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='imagenes_publicaciones',
            name='url_imagen',
            field=models.ImageField(blank=True, null=True, upload_to='imagenesPublicadas/', verbose_name='imageneURL'),
        ),
    ]