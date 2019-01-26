from django.contrib import admin
from django.contrib.auth.models import Group
# Register your models here.
from quiz.models import Question, Quiz, subTopic, Subject, Student, Answer, Summary, QuestionPost
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Student



@admin.register(QuestionPost)
#admin.site.register(Summary)
@admin.register(Quiz)
#admin.site.register(Question)
@admin.register(Answer)
@admin.register(Subject)
@admin.register(subTopic)
@admin.register(Student)
@admin.register(Summary)
@admin.register(Question)
class PersonAdmin(ImportExportModelAdmin):
    pass


