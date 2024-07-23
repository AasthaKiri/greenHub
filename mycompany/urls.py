from django.urls import path
from mycompany import views

urlpatterns = [
    path('about_us/', views.about_us, name='about_us'),
    path('success/', views.success, name='success'),  # Ensure this exists
    # Add other paths here
]
