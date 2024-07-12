from django.urls import path
from myapp import views

app_name = 'myapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),  # Define the URL pattern name
    path('<int:book_id>/', views.detail, name='detail'),  # Add this path
    path('feedback/', views.getFeedback, name='feedback1'),
    path('findbooks/', views.findbooks, name='findbooks'),
    path('place_order /', views.place_order, name='place_order'),
    path('submit_review/', views.submit_review, name='submit_review'),
    path('review/', views.review, name='review'),

]
