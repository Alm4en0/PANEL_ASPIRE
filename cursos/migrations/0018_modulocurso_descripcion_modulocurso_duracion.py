# Generated by Django 5.0.4 on 2024-06-16 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0017_delete_registroslanding_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='modulocurso',
            name='descripcion',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='modulocurso',
            name='duracion',
            field=models.DurationField(null=True),
        ),
    ]