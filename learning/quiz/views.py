from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from . import views
from django.contrib.auth.mixins import LoginRequiredMixin
from quiz.models import *
from django.views import generic
from django.views.generic import TemplateView, ListView, DetailView
from quiz.forms import QuestionForm
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


class StudentQuizListView(LoginRequiredMixin, generic.ListView):
    context_object_name = 'quiz_list'
    model = Student

    template_name ='quiz_list.html'
    paginate_by = 5
    def get_queryset(self, **kwargs):
        student = self.request.user.student
        queryset = student.assigned_quizzes.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(StudentQuizListView, self).get_context_data(**kwargs)
        context["quizzes"] = Student.assigned_quizzes
        return context
    


class StudentQuizDetailView(DetailView):
    model = Quiz
    template_name ='quiz/quiz_detail.html'

class QuestionQuizListView(ListView):
    context_object_name = 'question_list'
    model = Question
    template_name ='question_list.html'

    def get_queryset(self, **kwargs):
        gotten = Quiz.objects.get(pk=self.kwargs.get('pk'))
        queryset = gotten.question_set.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(QuestionQuizListView ,self).get_context_data(**kwargs)
        context["questions"] = Question.question_text
        return context
    
class QuestionQuizDetailView(DetailView):
    model = Question
    template_name = "quiz/question_detail.html"

    def get(self , request, *args, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        ques = Question.objects.get(pk = pk)
        # creating the form here
        form = QuestionForm()
        context = {'question_select': ques, 'form': form}
        return self.render_to_response(context)
    
    def post(self, request, *args, **kwargs):
        #pk = self.kwargs.get(self.pk_url_kwarg, None)
        form = QuestionForm(request.POST)
        if form.is_valid():
            QuestionPost = form.save(commit= False)
            QuestionPost.user = request.user.student
            QuestionPost.save()
            answer = form.cleaned_data['post']
            form = QuestionForm()
        arg = {'form': form, 'answer': answer}
        return render(request, self.template_name, arg)

    #def get_data(self, request):
    #    return render(request, self.template_name, {'form':form})
    
     

        

      

    
    



# this view
#  shall be on this file (do this by sunday)
# quiz (sat)
# quiz list page (sat)
# quiz detail page (sat)
# quiz questions (sun)
# quiz done page and score page (sun)
# finished quiz page (sun)
# quiz progess?
# (wed)


# this view shall be on another file (mon)
# student
# report on quizzes page
# performance page
# profile page
#(fri)

# this view shall too be on another file (thurs - sat)
# teacher
# create quiz page
# quiz list page
# performance for each quiz page
# performance per student page
# class page
#(sun)

#week 3
#machine learning?