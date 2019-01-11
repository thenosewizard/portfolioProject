from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from . import views
#from quiz.models import *


# Create your views here.

#this function returns the homepage
def index(request):
    
    return render(request, 'index.html', context = None)

def register(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        username1 = form.cleaned_data.get('username')
        password1 = form.cleaned_data.get('password1')
        user = authenticate(username = username1, password = password1)
        login(request, user)
        return redirect('index')
    context = {'form': form}
    return render(request, 'registerUser.html', context)
