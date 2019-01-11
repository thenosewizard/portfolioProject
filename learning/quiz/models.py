#from django.conf import settings
from django.db import models
from django.urls import reverse
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
    topic = models.ForeignKey(Subject,on_delete=models.CASCADE, null = True)
    date_created = models.DateField(auto_now = True)
    pass_mark = models.SmallIntegerField( blank=True, null=True, verbose_name = ("Pass mark"), validators = [MaxValueValidator(100)]) # validates the maximum mark set

    class Meta:
        pass


    #define a function here that get how many qns the user got correct
    def result(self, ):
        pass

    def __str__(self):
        return f'{self.quiz_name}'

    def get_absolute_url(self):
        return reverse("quiz-detail", args=[str(self.id)])
        

class Question(models.Model):
    sub_category = models.ForeignKey(subTopic, on_delete = models.CASCADE)
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
    related_question = models.name = models.ForeignKey(Question, on_delete=models.CASCADE)
    content_answer = models.CharField(max_length=500, help_text='Enter answer text here to display')
    correctAns =  models.BooleanField(blank=False, default = False , help_text ="Set if this is the correct Answer")

   #Methods
    def get_absolute_url(self):
        return reverse('answer-detail', args=[str(self.id)])

    def __str__(self):
        return self.content_answer


class TrackProgess(models.Model):
    """Model definition for MODELNAME.
    This model is to save the score of users taing the test
    So that we may calucate and do stuff with their scores
    """

    
    
    class Meta:
        """Meta definition for MODELNAME."""

        verbose_name = 'MODELNAME'
        verbose_name_plural = 'MODELNAMEs'

    def __str__(self):
        """Unicode representation of MODELNAME."""
        pass


#user
#report
#store progess of users (profile)
#sitting mangaer?


