from django.contrib import admin
from django.urls import path,include
from app import views

urlpatterns = [
    path('',views.home,name='home'),
    path('index/',views.index , name='index'),
    path('about/',views.about , name='about'),
    path('company/',views.company , name='company'),
    path('contact/',views.contact , name='contact'),
    path('login/',views.login , name='login'),
    path('shop/',views.shop , name='shop'),
    path('search/', views.product_search, name='product_search'),
    path('fav-search/', views.fav_product_search, name='fav_product_search'),
    path('add-to-favorites/<int:product_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('favorites/', views.view_favorites, name='view_favorites'),
    path('favorites_sort/', views.fav_product_sort, name='fav_product_sort'),
    path('del-favorites/<int:product_id>/', views.del_from_faves, name='del-favorites'),
    ]

