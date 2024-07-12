from django.shortcuts import render, HttpResponse
from myapp import models
# Create your views here.
def index(request):
    # return HttpResponse("Helloa")
    content = {'name':'Aastha','id':'12345'}
    return render(request, 'home.html',content)



