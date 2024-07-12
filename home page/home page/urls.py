"""
URL configuration for mysiteS24 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin # import statment
from django.urls import path, include # import statment

urlpatterns = [

    path('admin/', admin.site.urls),#  the URL for the admin interface
    # path('myapp/', include('myapp.urls1')),#  includes URLs defined in the 'myapp' application
    path('myapp/', include('myapp.urls')),
]
