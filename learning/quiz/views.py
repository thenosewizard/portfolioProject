from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from . import views
from django.contrib.auth.mixins import LoginRequiredMixin
from quiz.models import *
from django.views import generic
from django.views.generic import TemplateView, ListView, DetailView
from quiz.forms import QuestionForm
from django.shortcuts import get_list_or_404, get_object_or_404
from django.http import HttpResponseRedirect
#from quiz.models import *
from quiz.admin import *


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

class studentReportView(LoginRequiredMixin, generic.ListView):
    context_object_name = "summary_list"
    model = Student
    template_name = "quiz/individual_list.html"
    
    def get_queryset(self,  **kwargs):
        student = self.request.user.student
        queryset = student.summary_set.all()
        return queryset
        
    


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
        # creating the form here
        form = QuestionForm()
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        ques = Question.objects.get(pk = pk)
        context = {'question_select': ques, 'form': form}
        return self.render_to_response(context)
    
    def post(self, request, *args, **kwargs):
        #pk = self.kwargs.get(self.pk_url_kwarg, None)
        form = QuestionForm(request.POST)
        if form.is_valid():
            pk = self.kwargs.get(self.pk_url_kwarg, None)
            ques = Question.objects.get(pk = pk)
            #getting the quiz
            current_student = self.request.user.student
            student = Student.objects.get(pk = current_student.id)

            #getting the student
            try:
                all_summary = Summary.objects.filter(student = student)
                actual_summary = all_summary.get(quiz = ques.quiz_assigned.id)
                actual_summary.quiz = ques.quiz_assigned
            except:
                actual_summary = Summary(student = current_student, quiz = ques.quiz_assigned)
                actual_summary.save()

            #getting the quiz

            #saving the form
            QuestionPost = form.save(commit= False)
            QuestionPost.user = request.user.student
            QuestionPost.record = actual_summary
            QuestionPost.questionDone = get_object_or_404(Question, pk= self.kwargs['pk'])
            QuestionPost.save()

            answer = form.cleaned_data['post']
            form = QuestionForm()
        arg = {'form': form, 'answer': answer}
        return render(request, self.template_name, arg)
        #return HttpResponseRedirect(reverse('question-list'))
    #def get_data(self, request):
    #    return render(request, self.template_name, {'form':form})
    

#for teachers
class ResultListView(ListView):
    model = Summary
    context_object_name = "result_list"
    template_name ='quiz/result_list.html'

    

class ResultDetailView(DetailView):
    model = Summary
    context_object_name = "result_detail"
    template_name = 'quiz/result_detail.html'

    # we use get_context_data
    
# view to display the reports 
class ReportView(DetailView):
    pass
        

      

    
    



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