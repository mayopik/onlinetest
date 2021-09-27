from django import forms
from django.forms import widgets
from testapp import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from testapp.models import MCQ, QuestionPaper, Student, Subject

class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model=Student
        fields=['student_type']

class RegistrationForm(UserCreationForm):
    email=forms.EmailField(required=True)
    firstname=forms.CharField(max_length=20, required=True)
    lastname=forms.CharField(max_length=20, required=True)

    class Meta:
        model=User
        fields=('username', 'email', 'firstname', 'lastname', 'password1', 'password2')
        labels={'username':'Username/Roll.No'}

    def save(self, commit=True):
        user=super(RegistrationForm, self).save(commit=False)
        user.email=self.cleaned_data['email']
        user.first_name=self.cleaned_data['firstname']
        user.last_name=self.cleaned_data['lastname']
        if commit:
        	user.save()
        return user

class LoginForm(forms.Form):
    username=forms.CharField(max_length=150, label="Username/Roll.No")
    password=forms.CharField(widget=forms.PasswordInput())

class AddSubjectForm(forms.ModelForm):
    class Meta:
        model=Subject
        fields=('subject_name', 'subject_code')
        labels={'subject_name':'Name of subject', 'subject_code':'Subject Code'}

class CreateTestForm(forms.ModelForm):
    class Meta:
        model=QuestionPaper
        fields=('date_time', 'duration', 'instructions')
        labels={'date_time':'Date and time of test'}

class AddMCQForm(forms.Form):
    question_text=forms.CharField(widget=forms.Textarea, required=True)
    assigned_marks=forms.IntegerField(required=True)
    correct_option=forms.CharField(max_length=100, required=True)

    def __init__(self, *args, **kwargs):
        number_of_choices=kwargs.pop('number_of_choices')
        super(AddMCQForm, self).__init__(*args, **kwargs)

        for i in range(number_of_choices):
            self.fields[f'option_{(i+1)}']=forms.CharField(max_length=100)