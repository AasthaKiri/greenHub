# mycompany/views.py
from django.shortcuts import render, redirect
from mycompany.forms import ContactForm


def about_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('success')  # Redirect to a success page or another view
    else:
        form = ContactForm()

    return render(request, 'mycompany/about_us.html', {'form': form})

def success(request):
    return render(request, 'mycompany/success.html')
