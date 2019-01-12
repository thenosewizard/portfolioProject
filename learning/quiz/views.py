from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from . import views
from django.contrib.auth.mixins import LoginRequiredMixin
from quiz.models import *
from django.views import generic
from django.views.generic import TemplateView, ListView
#from quiz.models import *


# Create your views here.

@login_required
#this function returns the homepage
def index(request):
    
    return render(request, 'index.html', context = None)

# this view allows the user to log into the website
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

# there are class based views
# there are function based views



# create student view
# create teacher view 
# create normal view page


class QuizListView(LoginRequiredMixin, generic.ListView):
    model = Quiz
    context_object_name = 'my_quiz_list'

    def test(self, request):
        current_user = request.user
        return current_user.id
    def get_queryset(self):
        return Student.objects.filter( )

    template_name ='quiz_list.html'
    paginate_by = 5



# this view shall be on this file (do this by sunday)
# quiz (sat)
# quiz list page (sat)
# quiz detail page (sat)
# quiz questions (sun)
# quiz done page and score page (sun)
# finished quiz page (sun)
# quiz progess?



# this view shall be on another file (mon)
# student
# report on quizzes page
# performance page
# profile page


# this view shall too be on another file (thurs - sat)
# teacher
# create quiz page
# quiz list page
# performance for each quiz page
# performance per student page
# class page


#week 3
#machine learning? 

