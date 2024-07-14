from django.urls import path
from green import views

app_name = 'green'

urlpatterns = [
    path('', views.index, name='index'),
]
