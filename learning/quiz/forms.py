from django import forms
from quiz.models import QuestionPost

class QuestionForm(forms.ModelForm):
    post = forms.CharField(max_length= 40, required=False)
    class Meta:
        model = QuestionPost
        fields = ('post', )

#create quiz form
#create report form
