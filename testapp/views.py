from typing import AsyncIterable
from testapp.models import Student, Subject
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, AddSubjectForm, StudentRegistrationForm, RegistrationForm

# Create your views here.

def index(request):
    if request.method=="POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            user=authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                if hasattr(user, 'student'): # If user is a student
                    return HttpResponseRedirect('studentHome')
                else: # if user is examiner
                    return HttpResponseRedirect('examinerHome')
            else:
                form.add_error(None, 'Username or password is wrong')
    else:
        form=LoginForm()
    return render(request, 'index.html', context={'form': form})

def register(request):
    if request.method=="POST":
        data=request.POST.copy()
        role=data.pop('role')
        form=RegistrationForm(data)
        if form.is_valid():
            user=form.save()
            login(request, user)
            if role[0]=='Student':
                return HttpResponseRedirect('registerStudent')
            else:
                return HttpResponseRedirect('examinerHome')
    else:
            form=RegistrationForm()
    return render(request, 'register.html', context={"form":form})

def registerStudent(request):
    if request.method=='POST':
        form=StudentRegistrationForm(request.POST)
        if form.is_valid():
            newStudent=Student(id=request.user.id, user=request.user, student_type=form.cleaned_data['student_type'])
            newStudent.save()
            return HttpResponseRedirect('studentHome')
    else:
        form=StudentRegistrationForm()

    context={
        'form': form,
    }

    return render(request, 'register_student.html', context)

@login_required
def studentHome(request):
    return HttpResponse('<h1>STUDENT HOME PAGE<h2>')

@login_required
def examinerHome(request):
    context=dict()
    subject_list=Subject.objects.filter(examiner=request.user)
    context['subject_list']=subject_list
    return render(request, 'examiner_home.html', context)

@login_required
def addSubject(request):
    if request.method=='POST':
        form=AddSubjectForm(request.POST)
        if form.is_valid():
            newSubject=Subject(examiner=request.user, subject_code=form.cleaned_data['subject_code'], subject_name=form.cleaned_data['subject_name'])
            newSubject.save()
            # return HttpResponseRedirect('subject')
            return HttpResponseRedirect('examinerHome')
    else:
        form=AddSubjectForm()
    return render(request, 'register_student.html', context={'form':form})