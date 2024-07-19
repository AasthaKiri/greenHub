from django.shortcuts import render, redirect, get_object_or_404
from .models import Product,Category,Favorite
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def home(request):
    return render(request, 'home.html')
def contact(request):
    return render(request, 'contact.html')
def about(request):
    return render(request, 'about.html')
def login(request):
    return render(request, 'login.html')
def company(request):
    return render(request, 'company.html')



def index(request):
    products = Product.objects.all()

    return render(request, 'index.html',{'products':products})


def shop(request):
    categories = Category.objects.all()  # Fetch all categories
    # products = Product.objects.all()  # Fetch all products
    sort_option = request.GET.get('sort', 'name_asc')

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
    return render(request, 'shop.html', {'products': products, 'categories': categories})





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
    favorite_products = [favorite.product for favorite in favorites]
    return render(request, 'fav.html', {'fav': favorite_products})

def del_from_faves(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Favorite.objects.filter(product=product).delete()
    return redirect('shop')