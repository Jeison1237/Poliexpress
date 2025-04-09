# Generated by Django 5.1.7 on 2025-04-09 05:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0006_alter_producto_vendedor'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perfil',
            name='direccion',
        ),
        migrations.AddField(
            model_name='perfil',
            name='fecha_nacimiento',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='perfil',
            name='genero',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='perfil',
            name='nombre_real',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='rol',
            field=models.CharField(choices=[('cliente', 'Cliente'), ('vendedor', 'Vendedor')], max_length=20),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='telefono',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='producto',
            name='vendedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
