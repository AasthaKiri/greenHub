from django.shortcuts import render, redirect
from .models import Event, Volunteer, Achievement, BlogPost
from .forms import VolunteerForm, NewsletterSubscriptionForm
from django.http import JsonResponse


def home(request):
    events_list = Event.objects.all().order_by('date')
    volunteers = Volunteer.objects.all()[:4]  # Fetching some volunteers
    achievements = Achievement.objects.all()
    blog_posts = BlogPost.objects.all()

    context = {
        'events': events_list,
        'volunteers': volunteers,
        'achievements': achievements,
        'blog_posts': blog_posts,
    }
    return render(request, 'index.html', context)


def newsletter_signup(request):
    if request.method == 'POST' and request.is_ajax():
        form = NewsletterSubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Thank you for subscribing to our newsletter!'}, status=200)
        else:
            return JsonResponse({'message': 'Invalid email address.'}, status=400)
    return JsonResponse({'message': 'Invalid request.'}, status=400)


def add_volunteer(request):
    if request.method == 'POST':
        form = VolunteerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('volunteers')
    else:
        form = VolunteerForm()
    return render(request, 'add_volunteer.html', {'form': form})