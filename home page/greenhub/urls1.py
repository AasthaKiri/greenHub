from django.urls import path # import statment
from myapp import views # import statment for importing views form views.py

app_name = 'myapp'

urlpatterns = [
    path('', views.index, name='index'), # just for the /myapp page
    path('about/', views.about, name='about'), # this url is to get the data which is there in myapp/about page
    path('<int:book_id>/', views.detail, name='detail') # this url is for giving input to the url based on ID

]
