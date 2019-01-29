#from django.conf import settings
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
#from django.utils import timezone
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.core.validators import MaxValueValidator
import csv
from django import forms
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from import_export import resources,widgets

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
    topic =  models.ForeignKey(Subject, on_delete= models.SET_NULL, null = True)

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
    sub_category = models.ForeignKey(subTopic, on_delete = models.SET_NULL, null = True, blank = True)
    question_text = models.CharField(max_length=500, verbose_name = ("Question"))
    quiz_assigned = models.ForeignKey(Quiz, on_delete = models.SET_NULL, null = True, blank=True)

    DIFF_CHOICES = (('Easy', 'Easy'),('Intermediate', 'Intermediate'),('Hard', 'Hard'))

    difficulty = models.CharField(choices = DIFF_CHOICES, max_length=50, blank = True)
    #checks if the ans is correct
    def check_correct(self, guessed):
        answer_set = Answer.objects.get(id = guessed)

        if answer_set.correctAns == True:
            return True
        else:
            return False


    def __str__(self):
        return f'{self.question_text} [{self.sub_category}]'

    def get_absolute_url(self):
        return reverse("question-detail", args=[str(self.id)])
    
  
        

class Answer (models.Model):
    related_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content_answer = models.CharField(max_length=500, help_text='Enter answer text here to display')
    correctAns =  models.BooleanField(blank=False, default = False , help_text ="Set if this is the correct Answer")

   #Methods
    def get_absolute_url(self):
        return reverse('answer-detail', args=[str(self.id)])

    #def __str__(self):
    #    return self.content_answer


class Student(models.Model):
    """Model definition for Student."""
    # TODO: Define fields here
    studentUser = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null = True)
    #placeholer name until auth is added
    assigned_quizzes = models.ManyToManyField(Quiz)

    #defining field for gender
    M = 'M'
    F = 'F'

    GENDER_SELECT =  (
        (M, 'Male'), 
        (F, 'Female'),
    )

    HIGHER_SELECT = (
        ('yes', 'yes'),
        ('no', 'no'),
    )

    ACTIVITIES_SELECT = (
         ('yes', 'yes'),
        ('no', 'no'),
    )

    SCH_SUPPORT = (
        ('yes', 'yes'),
        ('no', 'no')
    )

    sex = models.CharField(max_length = 1, choices = GENDER_SELECT, default = M)

    age = models.IntegerField(null = True)
    travelTime = models.IntegerField(null = True)
    studytime = models.IntegerField(null= True)
    higher = models.CharField(max_length = 3, choices = HIGHER_SELECT, blank = True, default = 'yes')
    activities = models.CharField(max_length = 3, choices = ACTIVITIES_SELECT , blank = True, default = 'yes')
    absences = models.IntegerField(null = True, blank = True)
    passed = models.IntegerField(null = True)
    schoolsup = models.CharField(max_length = 3, choices = SCH_SUPPORT , blank = True, default = 'yes')
    freetime = models.IntegerField(default = 0)


    


    class Meta:
        pass
    
    def get_absolute_url(self):
        return reverse('student-detail', args=[str(self.id)])

    def __str__(self):
        """Unicode representation of Student."""
        return f'{self.studentUser.first_name}'




#saves score and date when the quiz is finished
class Summary(models.Model):
    """Model definition for Finished_quiz."""
    # TODO: Define fields here
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null = True)
    quiz = models.ForeignKey(Quiz, on_delete =  models.CASCADE, null = True)
    studentScore = models.IntegerField(default = 0)
    date_taken  = models.DateField(auto_now=True)

    class Meta:
        """Meta definition for Finished_quiz."""
        verbose_name = 'Finished_quiz'
        verbose_name_plural = 'Finished_quizzes'


    def get_totalScore(self):
        count = 0
        all_qns = self.questionpost_set.all()
        for i in range(len(all_qns)):
            if all_qns[i].check_correct(all_qns[i].id) == True:
                count += 1
        return count
    
    def check_passed(self):
        check_quiz = self.quiz
        passMark = check_quiz.pass_mark
        if passMark > self.get_totalScore():
            return False
        else:
            self.student.passed += 1
            return True

    # Summary.objects.all()[4].questionpost_set.all()[2].questionDone.sub_category.topic.subject_name        
    def get_weakness(self):
        weakness = []
        strengths = []

        topic = []
        topic_2 = []
        all_qns = self.questionpost_set.all()
        for i in range(len(all_qns)):

            if all_qns[i].check_correct(all_qns[i].id) == False:

                getting_post = all_qns[i].questionDone.sub_category.topic.subject_name
                weakness.append(getting_post)
            elif all_qns[i].check_correct(all_qns[i].id):
                getting_post = all_qns[i].questionDone.sub_category.topic.subject_name
                strengths.append(getting_post)

        try:
            for i in range(len(weakness)):
                if weakness.count(weakness[i]) > strengths.count(weakness[i]):
                    if weakness[i] in topic:
                        continue
                    else:
                        topic.append(weakness[i])
                else:
                    if weakness[i] in topic_2:
                        continue
                    else:
                        topic_2.append(weakness[i])
        except:
            for i in range(len(weakness)):
                if weakness[i] in topic_2:
                        continue
            else:
                topic.append(weakness[i])

        return topic
    
    def get_strength(self):
        weakness = []
        strengths = []

        topic = []
        topic_2 = []
        all_qns = self.questionpost_set.all()
        for i in range(len(all_qns)):

            if all_qns[i].check_correct(all_qns[i].id) == False:

                getting_post = all_qns[i].questionDone.sub_category.topic.subject_name
                weakness.append(getting_post)
            elif all_qns[i].check_correct(all_qns[i].id):
                getting_post = all_qns[i].questionDone.sub_category.topic.subject_name
                strengths.append(getting_post)
        
        try:
            for i in range(len(strengths)):
                if  strengths.count(strengths[i]) > weakness.count(strengths[i]):
                    if weakness[i] in topic_2:
                        continue
                    else:
                        topic_2.append(strengths[i])
                else:
                    if weakness[i] in topic:
                        continue
                    else:
                        topic.append(strengths[i])
        except:
            for i in range(len(strengths)):
                if strengths[i] in topic_2:
                        continue
                else:
                    topic_2.append(strengths[i])

        return topic_2


    def get_absolute_url(self):
        return reverse("result-detail", args=[str(self.id)])
    
    def __str__(self):
        """Unicode representation of Finished_quiz."""
        return f'{self.student} [{self.quiz}]'
        


class QuestionPost(models.Model):
    post = models.CharField(max_length=50)
    record = models.ForeignKey(Summary, on_delete = models.CASCADE, null =True)
    questionDone = models.ForeignKey(Question, on_delete = models.CASCADE , null = True)
    user = models.ForeignKey(Student, on_delete = models.CASCADE)

    def check_correct(self, guess):
        got_ans = QuestionPost.objects.get(pk = guess)
        ans = got_ans.post
        ques = Question.objects.get(pk = got_ans.questionDone.id)
        answers = ques.answer_set.all()

        count = 0
        for i in range(len(answers)):
            if ans == answers[i].content_answer and answers[i].correctAns == True:
                count +=1

        if count == 0:
            return False
        else:
            return True

    def __str__(self):
       return f'Question: {self.questionDone} Ans:({self.post})'
            

    


#Added to show a report of every student 
class Report(models.Model):
    #Added to show a report of every student 
    """Model definition for Report."""

    # TODO: Define fields here
    
    class Meta:
        #Added to show a report of every student 
        """Meta definition for Report."""

        verbose_name = 'Report'
        verbose_name_plural = 'Reports'


    def __str__(self):
        """Unicode representation of Report."""
        pass


#to test the machine learning model
class machineLearn(models.Model):
    sex = models.CharField( max_length=50)
    age = models.IntegerField(default = 0)
    travelTime = models.IntegerField(default = 1)
    studytime = models.IntegerField(default = 0)
    failures = models.IntegerField(default = 0)
    schoolsup = models.CharField(max_length=3)
    activities = models.CharField(max_length= 3)
    higher = models.CharField(max_length= 3)
    freetime = models.IntegerField(default = 0)
    absences = models.IntegerField(default = 0)
    passed = models.CharField(max_length=3)

    
    ordering = ['id','sex','age','travelTime','studytime','failures','schoolsup','activities','higher','freetime','absences','passed']
    #def __str__(self):
    #    pass
    
# use this to dump the data into this model
class pumpModel(models.Model):
    needHelp = models.CharField(max_length= 100)

    def __str__(self):
        return f'{self.id} [{self.needHelp}]'
    
    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('', kwargs={'pk': self.pk})


#Model to identify students who need help
class identify(models.Model):
    HELP_OPTIONS = (
        ('yes', 'yes'),
        ('no', 'no')
    )
    student = models.OneToOneField(Student, on_delete=models.CASCADE, null = True)
    help_needed = models.CharField(choices = HELP_OPTIONS, max_length=50, blank = True)

    def __str__(self):
        return f'{self.student} Help:[{self.help_needed}]'
    
    def get_absolute_url(self):
        return reverse("quiz-detail", args=[str(self.id)])


# Study model 
# student can request for a timetable
class studyModel(models.Model): 
    Student = models.ForeignKey(Student, null = True, on_delete =  models.CASCADE)
    DAY_SELECT = (
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'), 
        ('Wed', 'Wednesday'), 
        ('Thurs', 'Thursday'), 
        ('Fri', 'Friday'), 
        ('Sat', 'Saturday'), 
        ('Sun', 'Sunday')
        )

    day = models.CharField(choices = DAY_SELECT, max_length=50)
    subject = models.ForeignKey(Subject, on_delete = models.CASCADE)
    hours = models.PositiveIntegerField(validators =[MaxValueValidator(24)])

    def get_absolute_url(self):
        return reverse("study_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f'{self.day} {self.subject} {self.hours}'



    



