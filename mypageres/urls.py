from django.urls import path
from mypageres import views

app_name = 'mypageres'

urlpatterns = [
    path('Registartionpage/', views.register, name='Registartionpage'),
]

