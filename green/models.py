from django.contrib.auth.models import User
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
    email = models.EmailField(max_length=254, unique=True)
    phone_number = models.CharField(max_length=15)
    reason = models.TextField(blank=True)
    image = models.ImageField(upload_to='volunteers/', default='volunteers/volunteer_image.jpg')

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    image = models.ImageField(upload_to='blogimg/', default='blogimg/blog_image.jpg')
    short_description = models.TextField()
    detail_url = models.URLField()

    def __str__(self):
        return self.title


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

class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name}{self.last_name}'


class Product(models.Model):
    name = models.CharField(max_length=100)
    # price = models.DecimalField(default=0,decimal_places=2,max_digits=6)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=250 , default='',blank=True, null=True)
    image = models.ImageField(upload_to='static/img/')
    link = models.CharField(max_length=250 , default='')
    def __str__(self):
        return f'{self.name}'


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address =models.CharField(max_length=100,default='',blank=True, null=True)
    phone = models.CharField(max_length=20,default='',blank=True, null=True)
    date_ordered = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.product}'


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