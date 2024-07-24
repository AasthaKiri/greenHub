from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
import datetime


class Event(models.Model):
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    date = models.DateField()
    image = models.ImageField(upload_to='events/', default='events/event_image.jpg')
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    link = models.CharField(max_length=250 , default='')


    def __str__(self):
        return self.title


class Volunteer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.BigIntegerField(
        validators=[RegexValidator(regex='^\d{10}$', message='Phone number must be exactly 10 digits long.')]
    )
    image = models.ImageField(upload_to='volunteer_images/', blank=True, null=True)
    reason = models.TextField()

    def __str__(self):
        return self.name



class Achievement(models.Model):
    title = models.CharField(max_length=200)
    count = models.IntegerField()
    icon_class = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    # price = models.DecimalField(default=0,decimal_places=2,max_digits=6)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=250 , default='',blank=True, null=True)
    image = models.ImageField(upload_to='static/img/')
    link = models.CharField(max_length=250 , default='')
    def __str__(self):
        return f'{self.name}'



class Favorite(models.Model):
    product = models.ManyToManyField(Product, related_name='favorites', blank=True)
    holder = models.OneToOneField(User,on_delete=models.CASCADE,related_name='cart_holder')


    def __str__(self):
        return str(self.holder)


class Company(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='company_images/')

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name