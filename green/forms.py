from django import forms
from .models import Volunteer, NewsletterSubscription
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class VolunteerForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ['name', 'role', 'image', 'bio']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
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


# class UserRegistrationForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#     confirm_password = forms.CharField(widget=forms.PasswordInput)
#     bio = forms.CharField(widget=forms.Textarea, required=False)
#     birth_date = forms.DateField(required=False, widget=forms.SelectDateWidget)
#     captcha = CaptchaField()
#     profile_picture = forms.ImageField(required=False)
#
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password', 'bio', 'birth_date', 'captcha', 'profile_picture']
#
#     def clean_password(self):
#         password = self.cleaned_data.get('password')
#         if len(password) < 8:
#             raise ValidationError('Password must be at least 8 characters long.')
#         if not any(char.isdigit() for char in password):
#             raise ValidationError('Password must contain at least one digit.')
#         if not any(char.isalpha() for char in password):
#             raise ValidationError('Password must contain at least one letter.')
#         return password
#
#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get("password")
#         confirm_password = cleaned_data.get("confirm_password")
#
#         if password != confirm_password:
#             raise forms.ValidationError("Passwords do not match")
