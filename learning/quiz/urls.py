from django.urls import path
from quiz.views import StudentQuizListView, StudentQuizDetailView, QuestionQuizListView, QuestionQuizDetailView, ResultDetailView, ResultListView, studentReportView

from . import views


urlpatterns = [
     path('', views.index, name= "index"),
     path('myquizzes/', views.StudentQuizListView.as_view(), name = "quiz-list"),
     path('myquizzes/<int:pk>', views.StudentQuizDetailView.as_view(), name = "quiz-detail"),
     path('myquizzes/<int:pk>/questions/', views.QuestionQuizListView.as_view(), name = "question-list"),
     # <int:pk_alt> is used to get the id of the question as using pk will clash with the other pk
     path(r"^questions/(?P<pk>\d+)/choices", views.QuestionQuizDetailView.as_view(), name = "question-detail"),
     path('summary/', views.ResultListView.as_view(), name = "result-list"),
     path('summary/<int:pk>/student/', views.ResultDetailView.as_view(), name = "result-detail"),
     path('test/', views.studentReportView.as_view(), name = "individual-list"),
]

