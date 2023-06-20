# Generated by Django 4.2 on 2023-06-08 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_producto_cant_min_prod_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='producto',
            options={'ordering': ['nom_prod'], 'verbose_name': 'Producto', 'verbose_name_plural': 'Productos'},
        ),
        migrations.RemoveField(
            model_name='producto',
            name='id',
        ),
        migrations.AlterField(
            model_name='producto',
            name='nom_prod',
            field=models.CharField(max_length=200, primary_key=True, serialize=False),
        ),
    ]
