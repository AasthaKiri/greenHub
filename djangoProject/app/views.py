from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from .models import Product

# Create your views here.
def home(request):
    return render(request, 'home.html')

def index(request):
    products = Product.objects.all()

    return render(request, 'index.html',{'products':products})
