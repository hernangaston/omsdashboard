# Generated by Django 3.1 on 2023-03-08 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supervisor', '0005_auto_20230306_0850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articulo',
            name='tiempo_estimado_produccion',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='articulo',
            name='tiempo_real_produccion',
            field=models.FloatField(default=0),
        ),
    ]
