from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()

class Volunteer(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    image = models.ImageField(upload_to='volunteers/')

class Achievement(models.Model):
    title = models.CharField(max_length=200)
    count = models.IntegerField()
    icon_class = models.CharField(max_length=50)

