# Generated by Django 5.0.3 on 2024-06-19 21:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0021_remove_ventapago_paypal_id_venta_monto_venta_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='venta',
            name='monto_venta',
        ),
        migrations.RemoveField(
            model_name='venta',
            name='paypal_id',
        ),
    ]