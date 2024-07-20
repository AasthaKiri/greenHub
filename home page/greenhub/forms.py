from django import forms
from .models import Book,Review
from myapp.models import Order


# class FeedbackForm(forms.Form):
#     FEEDBACK_CHOICES = [
#         ('B', 'Borrow'),
#         ('P', 'Purchase'),
#     ]
#     feedback =   forms.ChoiceField(choices = FEEDBACK_CHOICES)

class FeedbackForm(forms.Form):
    FEEDBACK_CHOICES = [
        ('B', 'Borrow'),
        ('P', 'Purchase'),
    ]
    feedback = forms.MultipleChoiceField(
        choices=FEEDBACK_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label='Select your preferences'
    )

# class SearchForm(forms.Form):
#     name = forms.CharField(max_length=100, required=False)
#     CATEGORY_CHOICES = [
#         ('S', 'Science & Tech'),
#         ('F', 'Fiction'),
#         ('B', 'Biography'),
#         ('T', 'Travel'),
#         ('O', 'Other')
#     ]
#     category = forms.ChoiceField(choices=CATEGORY_CHOICES, widget=forms.RadioSelect)



class SearchForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=False,
        label='Your Name'
    )
    CATEGORY_CHOICES = [
        ('S', 'Science & Tech'),
        ('F', 'Fiction'),
        ('B', 'Biography'),
        ('T', 'Travel'),
        ('O', 'Other')
    ]
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.RadioSelect,
        required=False,
        label='Select a category:'
    )
    max_price = forms.IntegerField(
        label='Maximum Price',
        min_value=0
    )

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['books', 'member', 'order_type']
        widgets = {'books': forms.CheckboxSelectMultiple(), 'order_type':forms.RadioSelect}
        labels = {'member': 'Member name', }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['reviewer', 'book', 'rating', 'comments']
        widgets = {
            'book': forms.RadioSelect,
        }
        labels = {
            'reviewer': 'Please enter a valid email',
            'rating': 'Rating: An integer between 1 (worst) and 5 (best)',
        }


# class data(forms.ModelForm):
#     class Meta:
#         model = Book
#         field = "__all__"