from django.urls import path
from quiz.views import (StudentQuizListView, StudentQuizDetailView, QuestionQuizListView, QuestionQuizDetailView, 
ResultDetailView, ResultListView, studentReportView, ReportAnalyticsView, RequestQuizView)
from django.conf import settings
from django.conf.urls.static import static

from . import views




urlpatterns = [
     path('', views.index, name= "index"),
     path('myquizzes/', views.StudentQuizListView.as_view(), name = "quiz-list"),
     path('myquizzes/<int:pk>', views.StudentQuizDetailView.as_view(), name = "quiz-detail"),
     path('myquizzes/<int:pk>/questions/', views.QuestionQuizListView.as_view(), name = "question-list"),
     # <int:pk_alt> is used to get the id of the question as using pk will clash with the other pk
     #path(r"^questions/(?P<pk>\d+)/choices", views.QuestionQuizDetailView.as_view(), name = "question-detail"),
     path("questions/<int:pk>/choices", views.QuestionQuizDetailView.as_view(), name = "question-detail"),
     path('summary/', views.ResultListView.as_view(), name = "result-list"),
     path('summary/<int:pk>/student/', views.ResultDetailView.as_view(), name = "result-detail"),
     path('test/', views.studentReportView.as_view(), name = "individual-list"),
     path('report/', views.ReportAnalyticsView.as_view(), name = "need-list"),
     path('request/', views.RequestQuizView.as_view(), name = "requestQuiz-list"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

