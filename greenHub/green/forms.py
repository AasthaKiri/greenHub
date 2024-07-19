from django import forms
from .models import Volunteer, NewsletterSubscription


class VolunteerForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ['name', 'role', 'image', 'bio']


class NewsletterSubscriptionForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscription
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control border-0 bg-secondary w-100 py-3 ps-4 pe-5',
                'placeholder': 'Enter your email'
            })
        }