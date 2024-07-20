from django.urls import path
from MyApp import views

app_name = 'MyApp'

urlpatterns = [
    path('Registartionpage/', views.register, name='Registartionpage'),
]

