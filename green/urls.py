from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib import admin
from green import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='index'),
    path('add-volunteer/', views.add_volunteer, name='add_volunteer'),
    path('newsletter-signup/', views.newsletter_signup, name='newsletter_signup'),
    path('shop/', views.shop, name='shop'),
    path('search/', views.product_search, name='product_search'),
    path('fav-search/', views.fav_product_search, name='fav_product_search'),
    path('add-to-favorites/<int:product_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('favorites/', views.view_favorites, name='view_favorites'),
    path('favorites_sort/', views.fav_product_sort, name='fav_product_sort'),
    path('del-favorites/<int:product_id>/', views.del_from_faves, name='del-favorites'),
    # Include other URL patterns here
]

