from django import forms
from .models import Volunteer, NewsletterSubscription,Contact
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



# class VolunteerForm(forms.ModelForm):
#     class Meta:
#         model = Volunteer
#         fields = ['name', 'email', 'phone_number', 'reason', 'image']
#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'form-control'}),
#             'email': forms.EmailInput(attrs={'class': 'form-control'}),
#             'phone_number': forms.IntegerField(attrs={'class': 'form-control'}),
#             'reason': forms.Textarea(attrs={'class': 'form-control'}),
#             'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
#         }
#

class VolunteerForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ['name', 'email', 'phone_number', 'reason', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.NumberInput(attrs={
                'class': 'form-control',
                'minlength': '10',
                'maxlength': '10',
                'oninput': "if(this.value.length > 10) this.value = this.value.slice(0, 10);"
            }),
            'reason': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
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


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control'}),
        }
