from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.models import User
from .models import UserProfile

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            profile = UserProfile(user=user, phone_number=form.cleaned_data.get('phone_number'), profile_picture=form.cleaned_data.get('profile_picture'), address=form.cleaned_data.get('address'))
            profile.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'Registartionpage.html', {'form': form})
