from django.contrib import admin
from .models import Achievement, BlogPost, Event, Volunteer, NewsletterSubscription

admin.site.register(Achievement)
admin.site.register(BlogPost)
admin.site.register(Event)
admin.site.register(Volunteer)
admin.site.register(NewsletterSubscription)