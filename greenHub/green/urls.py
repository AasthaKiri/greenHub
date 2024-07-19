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
    # Include other URL patterns here
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
