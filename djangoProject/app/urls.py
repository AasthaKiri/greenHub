from django.contrib import admin
from django.urls import path,include
from app import views

urlpatterns = [
    path('',views.home,name='home'),
    # path('login/',views.login,name='login'),
    # path('register/',views.register,name='register'),
    # path('company/',views.company,name='company'),
    path('index/',views.index , name='index'),
]
