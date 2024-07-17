# Generated by Django 5.0.6 on 2024-07-17 20:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_product_image_favorite'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favorite',
            name='products',
        ),
        migrations.AddField(
            model_name='favorite',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.product'),
            preserve_default=False,
        ),
    ]
