# Generated by Django 5.0.7 on 2024-07-19 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('green', '0002_blogpost_newslettersubscription_remove_event_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(default='media/events/event_image.jpg', upload_to='media/events/'),
        ),
    ]
