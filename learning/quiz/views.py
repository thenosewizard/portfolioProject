from django.shortcuts import render
#from quiz.models import *


# Create your views here.

#this function returns the homepage
def index(request):
    
    return render(request, 'index.html', context = None)