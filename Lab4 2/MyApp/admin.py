from django.contrib import admin
from .models import Publisher, Book, Order, Member

# Register your models here.
admin.site.register(Publisher)
admin.site.register(Book)
admin.site.register(Order)
admin.site.register(Member)