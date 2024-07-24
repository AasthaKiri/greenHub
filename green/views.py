from django.db.models import Q
from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
# from .models import Product, Category, Favorite
from .models import Event, Volunteer, Achievement, Product, Category, Favorite, Company
from .forms import VolunteerForm, NewsletterSubscriptionForm, ContactForm
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str, force_bytes
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.mail import EmailMessage
from django.core.exceptions import ObjectDoesNotExist
import certifi
import smtplib
import ssl

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
import logging



# def home(request):
#     events_list = Event.objects.all().order_by('date')
#     volunteers = Volunteer.objects.all()[:4]  # Fetching some volunteers
#     achievements = Achievement.objects.all()
#
#     context = {
#         'events': events_list,
#         'volunteers': volunteers,
#         'achievements': achievements,
#     }
#     return render(request, 'index.html', context)
#

def home(request):
    # Fetching events, volunteers, and achievements
    events_list = Event.objects.all().order_by('date')
    volunteers = Volunteer.objects.all()[:4]  # Fetching some volunteers
    achievements = Achievement.objects.all()

    # Get the visit count from the session, or initialize it to 0 if it doesn't exist
    visit_count = request.session.get('visit_count', 0)
    visit_count += 1  # Increment the visit count
    request.session['visit_count'] = visit_count  # Save the updated visit count in the session

    context = {
        'events': events_list,
        'volunteers': volunteers,
        'achievements': achievements,
        'visit_count': visit_count,  # Pass the visit count to the template
    }

    return render(request, 'index.html', context)


def events(request):
    search_query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'date')

    # Get the current user's visit history from the session
    visit_history = request.session.get('event_visit_history', [])

    # Add the current search query to the visit history if it's not already present
    if search_query and search_query not in visit_history:
        visit_history.append(search_query)
        request.session['event_visit_history'] = visit_history

    events_list = Event.objects.all()

    # Filter events based on the search query
    if search_query:
        events_list = events_list.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )

    # Sort events based on the selected sorting option
    if sort_by == 'title':
        events_list = events_list.order_by('title')
    elif sort_by == 'location':
        events_list = events_list.order_by('location')
    else:  # Default to sorting by date
        events_list = events_list.order_by('date')

    event_paginator = Paginator(events_list, 9)  # Show 9 events per page
    event_page = request.GET.get('page')

    try:
        events_p = event_paginator.page(event_page)
    except PageNotAnInteger:
        events_p = event_paginator.page(1)
    except EmptyPage:
        events_p = event_paginator.page(event_paginator.num_pages)

    volunteers = Volunteer.objects.all()
    # Provide suggestions based on the visit history
    suggestions = [search for search in visit_history if search.lower().startswith(search_query.lower())]

    context = {
        'events': events_p,
        'search_query': search_query,
        'sort_by': sort_by,
        'visit_history': visit_history,
        'suggestions': suggestions,
        'volunteers': volunteers
    }

    return render(request, 'events.html', context)


def volunteer(request):
    volunteers = Volunteer.objects.all()
    return render(request, 'base1.html', {'volunteers': volunteers})


@require_POST
def newsletter_signup(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = NewsletterSubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Thank you for subscribing to our newsletter!'}, status=200)
        else:
            return JsonResponse({'message': 'Invalid email address.'}, status=400)
    return JsonResponse({'message': 'Invalid request.'}, status=400)


@login_required(login_url='login')
def add_volunteer(request):
    if request.method == 'POST':
        form = VolunteerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully registered as a volunteer!')
            return redirect('add_volunteer')
        else:
            messages.error(request, 'There was an error in registering. Please try again.')
    else:
        form = VolunteerForm()
    volunteers = Volunteer.objects.all()
    return render(request, 'add_volunteer.html', {'form': form, 'volunteers': volunteers})


def shop(request):
    categories = Category.objects.all()  # Fetch all categories
    selected_category_id = request.GET.get('category', None)
    sort_option = request.GET.get('sort', 'name_asc')
    query = request.GET.get('search', '')

    # Filter products by category if a category is selected
    if selected_category_id:
        selected_category = get_object_or_404(Category, id=selected_category_id)
        products = Product.objects.filter(category=selected_category)
    else:
        products = Product.objects.all()  # Fetch all products if no category is selected

    # Further filter products by search query if provided
    if query:
        products = products.filter(name__icontains=query)

    # Sort products based on the selected sorting option
    if sort_option == 'name_asc':
        products = products.order_by('name')  # Ascending order by product name
    elif sort_option == 'name_desc':
        products = products.order_by('-name')  # Descending order by product name

    paginator = Paginator(products, 9)  # Show 9 products per page
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    favorite_products = []
    if request.user.is_authenticated:
        try:
            favorite_products = Favorite.objects.get(holder=request.user).product.all()
        except Favorite.DoesNotExist:
            favorite_products = []

    #favorite_products = Favorite.objects.get(holder=request.user)
    volunteers = Volunteer.objects.all()
    context = {
        'products': products,
        'categories': categories,
        'selected_category_id': selected_category_id,
        'sort_option': sort_option,
        'query': query,
        'fav_products': favorite_products,
        #'fav_products': favorite_products.product.all(),
        'volunteers': volunteers

    }

    return render(request, 'shop.html', context)


@login_required(login_url='login')
def fav_product_sort(request):
    sort_option = request.GET.get('sort', 'name_asc')
    favorites = Favorite.objects.get(holder=request.user)

    if sort_option == 'name_asc':
        favorite_products = favorites.product.order_by('name')
    else:
        favorite_products = favorites.product.order_by('-name')

    paginator = Paginator(favorite_products, 9)  # Show 9 products per page
    page = request.GET.get('page')
    try:
        favorite_products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        favorite_products = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        favorite_products = paginator.page(paginator.num_pages)

    context = {
        'products': favorite_products,
        'sort': sort_option,
        'paginator': paginator,
        'page_obj': favorite_products,
    }
    return render(request, 'fav.html', context)


def product_search(request):
    query = request.GET.get('search', '')

    # Get the current user's visit history from the session
    visit_history = request.session.get('visit_history', [])

    # Add the current search query to the visit history if it's not already present
    if query and query not in visit_history:
        visit_history.append(query)
        request.session['visit_history'] = visit_history

    # Filter products based on the search query
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    # Provide suggestions based on the visit history
    suggestions = [search for search in visit_history if search.lower().startswith(query.lower())]

    context = {
        'products': products,
        'query': query,
        'visit_history': visit_history,
        'suggestions': suggestions,
    }

    return render(request, 'shop.html', context)


@login_required(login_url='login')
def fav_product_search(request):
    query = request.GET.get('search', '')
    favorites = Favorite.objects.get(holder=request.user)
    favorite_all = favorites.product.all()
    if query:
        favorite_products = favorites.product.filter(name__icontains=query)
    else:
        favorite_products = favorites.product.all()

    context = {
        'products': favorite_products,
        'query': query,
    }
    return render(request, 'fav.html', context)


@login_required(login_url='login')
def view_favorites(request):
    categories = Category.objects.all()  # Fetch all categories
    selected_category_id = request.GET.get('category', None)
    query = request.GET.get('search', '')

    # Get all favorite products for the current user
    try:
        favorites = Favorite.objects.get(holder=request.user)
    except Favorite.DoesNotExist:
        favorites = Favorite(holder=request.user)
        favorites.save()
    favorite_products = favorites.product.all()

    # Filter favorite products by category if a category is selected
    if selected_category_id:
        selected_category = get_object_or_404(Category, id=selected_category_id)
        favorite_products = favorite_products.filter(category=selected_category)

    # Filter favorite products by search query if provided
    if query:
        favorite_products = favorite_products.filter(name__icontains=query)

    context = {
        'fav': favorite_products,
        'categories': categories,
        'selected_category_id': selected_category_id,
        'query': query,
    }

    return render(request, 'fav.html', context)


@login_required(login_url='login')
def add_to_favorites(request, product_id):
    try:
        favorites = Favorite.objects.get(holder=request.user)
    except:
        favorites = Favorite()
        favorites.holder = request.user
        favorites.save()
    product = get_object_or_404(Product, id=product_id)

    if product in favorites.product.all():
        messages.error(request, "Product is already in the cart!")
        return redirect('view_favorites')

    else:
        favorites.product.add(product_id)
        favorites.save()
        return redirect('view_favorites')


@login_required(login_url='login')
def del_from_faves(request, product_id):
    favorites = Favorite.objects.get(holder=request.user)
    favorites.product.remove(product_id)
    favorites.save()
    return redirect('view_favorites')


def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return HttpResponse("Your password and confirm password are not Same!!")

        if User.objects.filter(username=uname).exists():
            messages.error(request, "Username already exists. Please choose a different one.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered. Please use a different email.")
            return redirect('signup')

        else:

            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            return redirect('login')

    return render(request, 'signup.html')

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return HttpResponse("Username or Password is incorrect!!!")

    return render(request, 'login.html')

@login_required(login_url='login')
def LogoutPage(request):
    logout(request)
    return redirect('login')


def password_reset_request(request):
    if request.method == "POST":
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)

            # Create a password reset token and send it to the user's email
            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

            # Send email with password reset link
            subject = 'Password Reset Request'
            message = render_to_string('password_reset_email.html', {
                'user': user,
                'domain': request.META['HTTP_HOST'],
                'uidb64': uidb64,
                'token': token,
            })
            from_email = settings.EMAIL_HOST_USER
            to_email = [user.email]

            # Create the email message
            email_message = EmailMessage(subject, message, from_email, to_email)

            # Encode the message as bytes
            message_as_bytes = message.encode('utf-8')

            # Configure SSL context with certifi
            context = ssl.create_default_context(cafile=certifi.where())
            try:
                with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
                    server.starttls(context=context)  # Secure the connection
                    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                    server.sendmail(from_email, to_email, message_as_bytes)
            except Exception as e:
                messages.error(request, 'Error sending email: {}'.format(e))
                return render(request, 'password_reset_request.html')

            messages.success(request, 'Password reset email has been sent.')
            return redirect('password_reset_done')
        else:
            messages.error(request, 'Email address not found. Please enter a valid email.')
            return render(request, 'password_reset_request.html')

    return render(request, 'password_reset_request.html')


def password_reset_done(request):
    return render(request, 'password_reset_done.html')

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        # Check if the token is valid for the user
        if default_token_generator.check_token(user, token):
            if request.method == 'POST':
                password1 = request.POST['password1']
                password2 = request.POST['password2']
                if password1 == password2:
                    user.set_password(password1)
                    user.save()
                    messages.success(request, 'Password reset successful. You can now login with your new password.')
                    return redirect('login')
                else:
                    messages.error(request, 'Passwords do not match. Please try again.')
                    return render(request, 'password_reset_confirm.html', {'uidb64': uidb64, 'token': token})
            return render(request, 'password_reset_confirm.html', {'uidb64': uidb64, 'token': token})
        else:
            messages.error(request, 'Password reset link is invalid or has expired. Please request a new one.')
            return redirect('password_reset_request')
    except Exception as e:
        print(e)
        messages.error(request, 'An error occurred. Please try again.')
        return redirect('password_reset_request')

def password_reset_complete(request):
    return render(request, 'password_reset_complete.html')

def about_us(request):
    volunteers = Volunteer.objects.all()

    return render(request, 'about.html', {'volunteers': volunteers})


def company(request):
    companies = Company.objects.all()
    volunteers = Volunteer.objects.all()

    return render(request, 'company.html', {'companies': companies, 'volunteers': volunteers})


def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for contacting us! Your message has been sent successfully!')
            return redirect('contact')
        else:
            messages.error(request, 'There was an error sending your message. Please try again.')
    else:
        form = ContactForm()
    volunteers = Volunteer.objects.all()

    return render(request, 'contact.html', {'form': form, 'volunteers': volunteers})
