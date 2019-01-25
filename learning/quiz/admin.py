from django.contrib import admin
from django.contrib.auth.models import Group

# Register your models here.
from quiz.models import Question, Quiz, subTopic, Subject, Student, Answer




admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Subject)
admin.site.register(subTopic)
admin.site.register(Student)