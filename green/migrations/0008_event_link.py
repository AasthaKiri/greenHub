# Generated by Django 5.0.6 on 2024-07-22 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('green', '0007_remove_product_price_product_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='link',
            field=models.CharField(default='', max_length=250),
        ),
    ]