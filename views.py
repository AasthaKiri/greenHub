# myapp/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            profile = user.profile
            profile.profile_picture = form.cleaned_data.get('profile_picture')
            profile.address = form.cleaned_data.get('address')
            profile.phone_number = form.cleaned_data.get('phone_number')
            profile.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'Registartionpage.html', {'form': form})
