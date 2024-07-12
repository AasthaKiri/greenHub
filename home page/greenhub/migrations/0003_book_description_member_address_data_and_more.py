# Generated by Django 5.0.6 on 2024-05-28 17:47

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_member'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='member',
            name='address_data',
            field=models.TextField(blank=True, max_length=300),
        ),
        migrations.AddField(
            model_name='publisher',
            name='country',
            field=models.CharField(blank=True, default='USA', max_length=20),
        ),
        migrations.AlterField(
            model_name='member',
            name='city',
            field=models.CharField(default='Windsor', max_length=20),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(0, 'Purchase'), (1, 'Borrow')], default=1)),
                ('order_date', models.DateField(default=django.utils.timezone.now)),
                ('books', models.ManyToManyField(to='myapp.book')),
                ('members', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.member')),
            ],
        ),
    ]
