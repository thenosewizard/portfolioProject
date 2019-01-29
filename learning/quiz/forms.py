from django import forms
from quiz.models import Subject, subTopic
from quiz.models import QuestionPost

class QuestionForm(forms.ModelForm):
    post = forms.CharField(max_length= 40, required=False)
    class Meta:
        model = QuestionPost
        fields = ('post', )

#create quiz form
#assign the quiz to the student
class RequestQuizForm(forms.Form):
    # so the user selects a quiz type 
    all_subjects = subTopic.objects
    SUBJECT_CHOICES = tuple(all_subjects.values_list('sub_topic_name', 'sub_topic_name'))
    sub_topic_name = forms.ChoiceField( choices = SUBJECT_CHOICES , required=False)

    #class Meta:
    #    model = Subject
    #    fields = ('Subject',)  




#create report form

#generate study plan form
