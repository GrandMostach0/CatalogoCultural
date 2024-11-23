# Generated by Django 5.1.1 on 2024-11-23 17:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0017_alter_actor_biografia_actor_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='redsocial',
            name='actor',
        ),
        migrations.AddField(
            model_name='redsocial',
            name='id_actor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalogo.actor', verbose_name='redes_sociales_Actor'),
        ),
    ]
