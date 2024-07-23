# Generated by Django 5.0.6 on 2024-07-23 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('green', '0008_event_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='company_images/')),
            ],
        ),
    ]
