from django import forms
from django.forms import widgets
from testapp import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from testapp.models import Student

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