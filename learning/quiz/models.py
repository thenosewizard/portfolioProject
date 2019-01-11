#from django.conf import settings
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
#from django.utils import timezone
#from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.core.validators import MaxValueValidator

#from django.utils.translation import ugettext as _
#from django.utils.timezone import now






# Create your models here.
class Subject(models.Model):
    subject_name = models.CharField(max_length=50)

    class meta:
        ordering = ['subject_name']

    def __str__(self):
        return self.subject_name


class subTopic(models.Model):
    sub_topic_name = models.CharField(max_length=50, )
    topic =  models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.sub_topic_name} ({self.topic})'


class Quiz(models.Model):
    quiz_name = models.CharField(max_length=50,  verbose_name = ("Quiz name"))
    description = models.CharField(max_length=500 , null = True)
    topic = models.ForeignKey(Subject,on_delete=models.SET_NULL, null = True)
    date_created = models.DateField(auto_now = True)
    pass_mark = models.SmallIntegerField( blank=True, null=True, verbose_name = ("Pass mark"), validators = [MaxValueValidator(100)]) # validates the maximum mark set


    class Meta:
        pass

    #string that can be used in the admin interface
    def __str__(self):
        return f'{self.quiz_name}'

    def get_absolute_url(self):
        return reverse("quiz-detail", args=[str(self.id)])
        

class Question(models.Model):
    sub_category = models.ForeignKey(subTopic, on_delete = models.SET_NULL, null = True)
    question_text = models.CharField(max_length=500, verbose_name = ("Question"))
    quiz_assigned = models.ManyToManyField(Quiz)

    #checks if the ans is correct
    def check_correct(self, guessed):
        answer_set = Answer.objects.get(id = guessed)

        if answer_set.correctAns == True:
            return True
        else:
            return False


    def __str__(self):
        return f'{self.question_text} ({self.sub_category})'

    def get_absolute_url(self):
        return reverse("question-detail", args=[str(self.id)])
        

class Answer (models.Model):
    related_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content_answer = models.CharField(max_length=500, help_text='Enter answer text here to display')
    correctAns =  models.BooleanField(blank=False, default = False , help_text ="Set if this is the correct Answer")

   #Methods
    def get_absolute_url(self):
        return reverse('answer-detail', args=[str(self.id)])

    def __str__(self):
        return self.content_answer


class Student(models.Model):
    """Model definition for Student."""
    # TODO: Define fields here

    #placeholer name until auth is added
    student_name = models.CharField(max_length=50, null = True)
    assigned_quizzes = models.ManyToManyField(Quiz, null = True)

    class Meta:
        pass

    def get_absolute_url(self):
        return reverse('student-detail', args=[str(self.id)])

    def __str__(self):
        """Unicode representation of Student."""
        return f'{self.student_name}'


class Finished_quiz(models.Model):
    """Model definition for Finished_quiz."""

    # TODO: Define fields here

    #student who did the quiz
    #quizzes that they have done
    #score for that quiz


    class Meta:
        """Meta definition for Finished_quiz."""

        verbose_name = 'Finished_quiz'
        verbose_name_plural = 'Finished_quizs'

    #def __str__(self):
    #    """Unicode representation of Finished_quiz."""
    #    pass


