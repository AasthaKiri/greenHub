
from django.http import HttpResponse
from .models import Publisher, Book, Member, Order
from django.shortcuts import get_object_or_404
from django.shortcuts import render # it may be already in your views.py file
from myapp.templates import myapp
from .forms import FeedbackForm, SearchForm,OrderForm,ReviewForm

# Create your views here.
# def index(request):
#     response = HttpResponse()
#
#     # Fetch and order the book list by id
#     data_books = Book.objects.all().order_by('id')
#     title_data1 = '<h1>' + 'List of Available Books: ' + '</h1>'
#     response.write(title_data1)
#     for book in data_books:
#         para = '<p>'+ str(book.id) + ': ' + str(book) + '</p>'
#         response.write(para)
#
#     # Fetch and order the publisher list by city name in descending order
#     data_publishers = Publisher.objects.all().order_by('-city')
#     title_data2 = '<h1>' + 'List of Publishers: ' + '</h1>'
#     response.write(title_data2)
#     for publisher in data_publishers:
#         para = '<p>' + str(publisher.name) + ' from city  ' + str(publisher.city) + '</p>'
#         response.write(para)
#
#
#     return response


def index(request):
    booklist = Book.objects.all().order_by('id')[:10]
    contect = {'booklist': booklist}  # storing the booklist in dictionary and passing that in render
    return render(request,'myapp/index0.html', contect)
# we are passing variable contect

# def about(request):
#     response = HttpResponse()
#     title_about_page = '<h2>' + ' This is an eBook Website ' + '</h2>'
#     orders = Order.objects.filter(order_type=0)
#     for ord in orders:
#         books = ord.books.all()
#         for books in books:
#
#             pur = books.title
#             name = books.title
#             publisher = books.publisher
#
#             response.write(pur+'<br>')
#             response.write(name)
#             response.write(publisher)
#
#     # response.write(title_about_page)
#
#     return response
# # No extra varibale has been pased

def about(request):
    title_about_page = '<h2>' + ' This is an eBook Website ' + '</h2>'
    return render(request,'myapp/about0.html')


def detail(request, book_id):
    books = get_object_or_404(Book, pk=book_id)
    contect = {'book':books} # storing the booklist in dictionary and passing that in render
    # response = HttpResponse()
    #
    # book_titl = '<h3>' + book.title.upper() + '</h3>'
    # response.write(book_titl)
    #
    # book_prc = '<p>' + 'Price: $' + str(book.price) + '</p>'
    # response.write(book_prc)
    #
    # book_pub = '<p>' + 'Publisher: ' + str(book.publisher) + '</p>'
    # response.write(book_pub)
    return render(request, 'myapp/detail0.html', contect)
    # YES we are passing contect varibale which is a dictionary of book data



    return response

# def getFeedback(request):
#     if request.method == 'POST':
#         form = FeedbackForm(request.POST)
#         if form.is_valid():
#             feedback = request.POST.get('feedback','')
#             if feedback == 'B':
#                 choice = ' to borrow books.'
#             elif feedback == 'P':
#                 choice = ' to purchase books.'
#             else: choice = ' None.'
#             return render(request, 'myapp/fb_results.html', {'choice':choice})
#         else:
#             return HttpResponse('Invalid data')
#     else:
#         form = FeedbackForm()
#         return render(request, 'myapp/feedback.html', {'form':form})


def getFeedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.cleaned_data['feedback']
            choices = [dict(FeedbackForm.FEEDBACK_CHOICES).get(choice) for choice in feedback]
            return render(request, 'myapp/fb_results.html', {'choices': choices})
        else:
            return HttpResponse('Invalid data')
    else:
        form = FeedbackForm()
        return render(request, 'myapp/feedback.html', {'form': form})

def searchBooks(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            name = request.POST.get('name','')
            category = request.POST.get('category','')
            books = Book.objects.filter(category=category)
            return render(request, 'myapp/search_results.html', {'books': books, 'name': name, 'category': category})
    else:
        form = SearchForm()
    return render(request, 'myapp/search.html', {'form': form})




# def findbooks(request):
#     if request.method == 'POST':
#         form = SearchForm(request.POST)
#         if form.is_valid():
#             name = form.cleaned_data['name']
#             category = form.cleaned_data['category']
#             booklist = Book.objects.filter(category=category)
#             return render(request, 'myapp/results.html', {'name': name, 'booklist': booklist})
#         else:
#             return HttpResponse('Invalid data')
#     else:
#         form = SearchForm()
#     return render(request, 'myapp/findbooks.html', {'form': form})



def findbooks(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            name = request.POST.get('name','')
            category = request.POST.get('category','')
            max_price = request.POST.get('max_price','')

            if category:
                # booklist = Book.objects.filter(category=category, price__lte=max_price)
                booklist = Book.objects.filter(category=category)
            # else:
            #     booklist = Book.objects.filter(price__lte=max_price)

            return render(request, 'myapp/results.html', {
                'name': name,
                'category': category,
                'booklist': booklist
                # 'max_price':max_price
            })
        else:
            return HttpResponse('Invalid data')
    else:
        form = SearchForm()
    return render(request, 'myapp/findbooks.html', {'form': form})



def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            books = form.cleaned_data['books']
            order = form.save(commit=False)
            member = order.member
            type = order.order_type
            order.save()
            form.save_m2m()
            if type == 1:
                for bok in order.books.all():
                    member.borrowed_books.add(bok)
            return render(request, 'myapp/order_response.html', {'books': books, 'order':order})
        else:
            return render(request, 'myapp/placeorder.html', {'form':form})

    else:
        form = OrderForm()
        return render(request, 'myapp/placeorder.html', {'form':form})

def submit_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,'myapp/review_success.html')  # Redirect to a success page
    else:
        form = ReviewForm()

    return render(request, 'myapp/submit_review.html', {'form': form})


def review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            if 1 <= rating <= 5:
                review = form.save(commit=False)
                review.save()
                book = review.book
                book.num_reviews += 1
                book.save()
                return render(request, 'myapp/index0.html')  # Redirect to the main (index.html) page
            else:
                return render(request, 'myapp/review.html', {'form': form, 'error_message': 'You must enter a rating between 1 and 5!'})
        else:
            return render(request, 'myapp/review.html', {'form': form})
    else:
        form = ReviewForm()
        return render(request, 'myapp/review.html', {'form': form})