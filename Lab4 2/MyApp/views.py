from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import UserRegistrationForm
from .models import Profile


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            user.save()
            profile = Profile.objects.create(
                user=user,
                bio=form.cleaned_data['bio'],
                birth_date=form.cleaned_data['birth_date'],
                profile_picture=form.cleaned_data['profile_picture']
            )
            profile.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'Registartionpagegit remo.html', {'form': form})
