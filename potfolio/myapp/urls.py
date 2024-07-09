from django.contrib import admin
from django.urls import path,include
from myapp import views

admin.site.site_header = "Hello"
admin.site.site_title = "welcome to this "
admin.site.index_title = "this is portal"

urlpatterns = [
    path('',views.index , name = 'home'),

    # path('',views.index , name = 'home'),
]