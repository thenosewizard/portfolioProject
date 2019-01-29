from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from . import views
import random
from django.contrib.auth.mixins import LoginRequiredMixin
from quiz.models import *
from django.views import generic
from django.views.generic import TemplateView, ListView, DetailView
from quiz.forms import QuestionForm, RequestQuizForm
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
            #return redirect('quiz-detail', pk= QuestionPost.questionDone.quiz_assigned.id )
            return redirect('question-list', pk= QuestionPost.questionDone.quiz_assigned.id )
        arg = {'form': form, 'answer': answer}
        #return HttpResponseRedirect(reverse('quiz-detail'))
        return render(request, self.template_name, arg)
    #def get_data(self, request):
    #    return render(request, self.template_name, {'form':form})
    

#for teachers
class ResultListView(ListView):
    model = Summary
    context_object_name = "result_list"
    template_name ='quiz/result_list.html'

    


# here is where students see their strength and weaknesses
class ResultDetailView(DetailView):
    model = Summary
    context_object_name = "result_detail"
    template_name = 'quiz/result_detail.html'

#    def get_queryset(self):
#        get = Summary.objects.filter(pk = self.kwargs.get('pk'))
#        weak = get.get_weakness
#        stren = get.get_strength

        #query = {'weak': weak, 'strength': stren}
        #return query

    def get_context_data(self, **kwargs):
        context = super(ResultDetailView ,self).get_context_data(**kwargs)
        get = Summary.objects.get(pk = self.kwargs.get('pk'))
        list_weak = get.get_weakness()
        list_str = get.get_strength()

        weak = ""
        strengths = ""
        for i in range(len(list_weak)):
            weak += list_weak[i]

        for i in range(len(list_str)):
            strengths += list_str[i]

        context = {'weak': weak, 'strengths': strengths, 'name': get.student, 'passed':get.check_passed, 'quiz':get.quiz, 'score': get.get_totalScore}
        return context
    
    
    # we use get_context_data
    
# view to display the reports 
class ReportAnalyticsView(ListView):
    model = identify
    context_object_name = "need_list"
    template_name = "quiz/need_list.html"
    
    


#generate quiz view 
#assign quiz to students 
class RequestQuizView(TemplateView):
    template_name = "quiz/requestQuiz_list.html"

    def get(self, request, *args, **kwargs):
        form = RequestQuizForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = RequestQuizForm(request.POST)

        if form.is_valid():
            choice = form.cleaned_data['sub_topic_name']
            choice = dict(form.fields['sub_topic_name'].choices)[choice]
            form = RequestQuizForm()

            current_student = self.request.user.student
            student = Student.objects.get(pk = current_student.id)

            category = subTopic.objects.get(sub_topic_name = choice)
            subject_get = category.topic
            questions = Question.objects.filter(sub_category = category.id)
            

            # check if user is [yes] or [no]
            student_help = identify.objects.get(student = current_student)
            check_help = student_help.help_needed

            num_questions = 0
            if check_help == 'yes':
                num_questions = 3
            else:
                num_questions = 2


            #generating a random quiz number to identify it
            number = random.randint(0, 1000000)
            # getting the questions that are not assigned to any quizzes
            question_list = []
            for i in range(len(questions)):
                # to prevent the user from getting all the qns and to keep his/her workload easy
                if not questions[i].quiz_assigned:
                    if len(question_list) > num_questions:
                        break
                    else:
                        question_list.append(questions[i])

            new_quiz = Quiz(quiz_name = f'{number}', topic = subject_get, pass_mark = len(question_list)/2)
            new_quiz.save()

            for i in range(len(question_list)):
                question_list[i].quiz_assigned = new_quiz
                question_list[i].save()
            
            student.assigned_quizzes.add(Quiz.objects.get(pk = new_quiz.id)) 

            #return redirect('index')
            args = {'form': form, 'choice':choice}
        return render(request, self.template_name, args)
    
class generateStudyView(ListView):
    pass

class DetailStudyView(ListView):
    pass
    
class StrengthAndWeakness(ListView):
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