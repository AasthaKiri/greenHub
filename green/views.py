from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product,Category,Favorite
from .models import Event, Volunteer, Achievement, BlogPost
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

    if selected_category_id:
        selected_category = get_object_or_404(Category, id=selected_category_id)
        products = Product.objects.filter(category=selected_category)
    else:
        products = Product.objects.all()  # Fetch all products if no category is selected

    if sort_option == 'name_asc':
        products = Product.objects.order_by('name')  # Ascending order by category name
    elif sort_option == 'name_desc':
        products = Product.objects.order_by('-name')  # Descending order by category name
    else:
        products = Product.objects.all()  # Default to displaying all products

    paginator = Paginator(products, 9)  # Show 9 products per page
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)

    favorite_products = Favorite.objects.all()

    # return render(request, 'shop.html', {'products': products, 'categories': categories})
    return render(request, 'shop.html', {
        'products': products,
        'categories': categories,
        'selected_category_id': selected_category_id,
        'sort_option': sort_option,
        'fav_products': [favorite.product for favorite in favorite_products]

    })




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

def view_favorites(request):
    favorites = Favorite.objects.all()
    categories = Category.objects.all()  # Fetch all categories

    favorite_products = [favorite.product for favorite in favorites]

    return render(request, 'fav.html', {'fav': favorite_products,'categories':categories})

def del_from_faves(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Favorite.objects.filter(product=product).delete()
    return redirect('view_favorites')

