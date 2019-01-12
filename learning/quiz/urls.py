from django.urls import path
from quiz.views import QuizListView

from . import views

urlpatterns = [
     path('', views.index, name= "index"),
     path('myquizzes/', views.QuizListView.as_view(), name = "quiz-list")

]
