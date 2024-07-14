from django.shortcuts import render
from .models import Event, Volunteer, Achievement


def home(request):
    events = Event.objects.all()[:3]  # Fetching recent events
    volunteers = Volunteer.objects.all()[:4]  # Fetching some volunteers
    achievements = Achievement.objects.all()

    context = {
        'events': events,
        'volunteers': volunteers,
        'achievements': achievements,
    }
    return render(request, 'index.html', context)


