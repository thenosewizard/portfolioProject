from django.urls import path
from quiz.views import StudentQuizListView, StudentQuizDetailView, QuestionQuizListView, QuestionQuizDetailView

from . import views


urlpatterns = [
     path('', views.index, name= "index"),
     path('myquizzes/', views.StudentQuizListView.as_view(), name = "quiz-list"),
     path('myquizzes/<int:pk>', views.StudentQuizDetailView.as_view(), name = "quiz-detail"),
     path('myquizzes/<int:pk>/questions/', views.QuestionQuizListView.as_view(), name = "question-list"),
     # <int:pk_alt> is used to get the id of the question as using pk will clash with the other pk
     path(r"^questions/(?P<pk>\d+)/choices", views.QuestionQuizDetailView.as_view(), name = "question-detail"),
]

