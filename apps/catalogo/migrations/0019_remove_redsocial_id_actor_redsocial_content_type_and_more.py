# Generated by Django 5.1.1 on 2024-11-23 19:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0018_remove_redsocial_actor_redsocial_id_actor'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='redsocial',
            name='id_actor',
        ),
        migrations.AddField(
            model_name='redsocial',
            name='content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='redsocial',
            name='object_id',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
