# Generated by Django 4.2 on 2023-06-10 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_producto_options_remove_producto_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='valor_total_prod',
            field=models.CharField(default=12, editable=False),
            preserve_default=False,
        ),
    ]
