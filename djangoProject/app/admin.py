from django.contrib import admin
from django.contrib.auth.models import User
from .models import Customer,Product,Order,Category,Favorite

# Register your models here
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Favorite)
