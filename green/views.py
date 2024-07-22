from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
# from .models import Product, Category, Favorite
from .models import Event, Volunteer, Achievement, BlogPost,Product, Category, Favorite
from .forms import VolunteerForm, NewsletterSubscriptionForm
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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


def events(request):
    events_list = Event.objects.all().order_by('date')
    event_paginator = Paginator(events_list, 9)  # Show 9 events per page
    event_page = request.GET.get('page')

    try:
        events_p = event_paginator.page(event_page)
    except PageNotAnInteger:
        events_p = event_paginator.page(1)
    except EmptyPage:
        events_p = event_paginator.page(event_paginator.num_pages)

    context = {
        'events': events_p,
    }
    return render(request, 'events.html', context)


def blog(request):
    blog_posts = BlogPost.objects.all()

    context = {
        'blog_posts': blog_posts,
    }
    return render(request, 'blogs.html', context)


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


def add_volunteer(request):
    if request.method == 'POST':
        form = VolunteerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('volunteers')
    else:
        form = VolunteerForm()
    return render(request, 'add_volunteer.html', {'form': form})


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

    favorite_products = Favorite.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'selected_category_id': selected_category_id,
        'sort_option': sort_option,
        'query': query,
        'fav_products': [favorite.product for favorite in favorite_products]
    }

    return render(request, 'shop.html', context)



def fav_product_sort(request):
    query = request.GET.get('search', '')
    sort_option = request.GET.get('sort', 'name_asc')

    if query:
        favorite_products = Favorite.objects.filter(product__name__icontains=query)
    else:
        favorite_products = Favorite.objects.all()

    if sort_option == 'name_asc':
        favorite_products = favorite_products.order_by('product__name')
    elif sort_option == 'name_desc':
        favorite_products = favorite_products.order_by('-product__name')

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
        'products': [favorite.product for favorite in favorite_products],
        'query': query,
        'sort': sort_option,
        'paginator': paginator,
        'page_obj': favorite_products,
    }
    return render(request, 'fav.html', context)


def product_search(request):
    query = request.GET.get('search', '')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'shop.html', context)


def fav_product_search(request):
    query = request.GET.get('search', '')
    if query:
        favorite_products = Favorite.objects.filter(product__name__icontains=query)
    else:
        favorite_products = Favorite.objects.all()

    context = {
        'products': [favorite.product for favorite in favorite_products],
        'query': query,
    }
    return render(request, 'fav.html', context)


def add_to_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if not Favorite.objects.filter(product=product).exists():
        Favorite.objects.create(product=product)
    return redirect('shop')  # Assuming 'shop' is the name of your product listing page


# def view_favorites(request):
#     favorites = Favorite.objects.all()
#     categories = Category.objects.all()  # Fetch all categories
#     selected_category_id = request.GET.get('category', None)
#
#     query = request.GET.get('search', '')
#
#     if selected_category_id:
#         selected_category = get_object_or_404(Category, id=selected_category_id)
#         products = Product.objects.filter(category=selected_category)
#     else:
#         products = Product.objects.all()  # Fetch all products if no category is selected
#
#     if query:
#         favorite_products = Favorite.objects.filter(product__name__icontains=query)
#     else:
#         favorite_products = Favorite.objects.all()
#
#     favorite_products = [favorite.product for favorite in favorites]
#
#     return render(request, 'fav.html', {'fav': favorite_products, 'categories': categories, 'query': query,
#                                         })
def view_favorites(request):
    categories = Category.objects.all()  # Fetch all categories
    selected_category_id = request.GET.get('category', None)
    query = request.GET.get('search', '')

    # Get all favorite products
    favorite_products = Favorite.objects.all()

    # Filter favorite products by category if a category is selected
    if selected_category_id:
        selected_category = get_object_or_404(Category, id=selected_category_id)
        favorite_products = favorite_products.filter(product__category=selected_category)

    # Filter favorite products by search query if provided
    if query:
        favorite_products = favorite_products.filter(product__name__icontains=query)

    # Extract the products from the favorite products queryset
    favorite_products = [favorite.product for favorite in favorite_products]

    context = {
        'fav': favorite_products,
        'categories': categories,
        'selected_category_id': selected_category_id,
        'query': query,
    }

    return render(request, 'fav.html', context)


def del_from_faves(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Favorite.objects.filter(product=product).delete()
    return redirect('view_favorites')



# def register(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST, request.FILES)
#         if form.is_valid():
#             user = User.objects.create_user(
#                 username=form.cleaned_data['username'],
#                 email=form.cleaned_data['email'],
#                 password=form.cleaned_data['password']
#             )
#             user.save()
#             profile = Profile.objects.create(
#                 user=user,
#                 bio=form.cleaned_data['bio'],
#                 birth_date=form.cleaned_data['birth_date'],
#                 profile_picture=form.cleaned_data['profile_picture']
#             )
#             profile.save()
#             login(request, user)
#             return redirect('home')
#     else:
#         form = UserRegistrationForm()
#     return render(request, 'Registartionpagegit remo.html', {'form': form})