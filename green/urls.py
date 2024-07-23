from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib import admin
from green import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='index'),
    path('add-volunteer/', views.add_volunteer, name='add_volunteer'),
    path('events/', views.events, name='events'),
    path('newsletter-signup/', views.newsletter_signup, name='newsletter_signup'),
    path('shop/', views.shop, name='shop'),
    path('search/', views.product_search, name='product_search'),
    path('fav-search/', views.fav_product_search, name='fav_product_search'),
    path('add-to-favorites/<int:product_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('favorites/', views.view_favorites, name='view_favorites'),
    path('favorites_sort/', views.fav_product_sort, name='fav_product_sort'),
    path('del-favorites/<int:product_id>/', views.del_from_faves, name='del-favorites'),
    path('signup/', views.SignupPage, name='signup'),
    path('login/', views.LoginPage, name='login'),
    path('logout/', views.LogoutPage, name='logout'),
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('password-reset/done/', views.password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', views.password_reset_complete, name='password_reset_complete'),
    path('about/',views.about_us,name='about'),
    path('company/',views.company,name='company'),
    path('contact/',views.contact_us,name='contact'),
    # path('category_shop/<int:category_id>/',views.shop,name='category')


]
