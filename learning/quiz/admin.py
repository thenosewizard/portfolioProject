from django.contrib import admin
from django.contrib.auth.models import Group
# Register your models here.
from quiz.models import Question, Quiz, subTopic, Subject, Student, Answer, Summary, QuestionPost, machineLearn, pumpModel
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Student
from import_export import resources,widgets
from import_export import resources,widgets
from import_export.fields import Field



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
@admin.register(pumpModel)
class PersonAdmin(ImportExportModelAdmin):
    pass



class machineLearnResource(resources.ModelResource):
    class Meta:
        model = machineLearn
        


@admin.register(machineLearn)
class SessionAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    resource_class = machineLearnResource