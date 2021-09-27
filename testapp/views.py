from typing import AsyncIterable
import datetime

from django.http.response import Http404
from testapp.models import Student, Subject, QuestionPaper
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, StudentRegistrationForm, RegistrationForm, AddSubjectForm, CreateTestForm

# Create your views here.

def index(request):
    if request.method=="POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            user=authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                if hasattr(user, 'student'): # If user is a student
                    return HttpResponseRedirect(reverse('student_home'))
                else: # if user is examiner
                    return HttpResponseRedirect(reverse('examiner_home'))
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
                return HttpResponseRedirect(reverse('register_student'))
            else:
                return HttpResponseRedirect(reverse('examiner_home'))
    else:
            form=RegistrationForm()
    return render(request, 'register.html', context={"form":form})

def registerStudent(request):
    if request.method=='POST':
        form=StudentRegistrationForm(request.POST)
        if form.is_valid():
            newStudent=Student(id=request.user.id, user=request.user, student_type=form.cleaned_data['student_type'])
            newStudent.save()
            return HttpResponseRedirect(reverse('student_home'))
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
            return HttpResponseRedirect(reverse('examiner_home'))
    else:
        form=AddSubjectForm()
    return render(request, 'register_student.html', context={'form':form})

@login_required
def viewSubject(request, sub_code):
    try:
        subject=Subject.objects.get(subject_code=sub_code)
    except Subject.DoesNotExist:
        raise Http404('Subject does not exist!')
    
    return render(request, 'view_subject.html', context={'subject':subject})

@login_required
def createTest(request, sub_code):
    try:
        subject=Subject.objects.get(subject_code=sub_code)
    except Subject.DoesNotExist:
        raise Http404('Subject does not exist!')
    
    if request.method=="POST":
        form=CreateTestForm(request.POST)
        if form.is_valid():
            newQPaper=QuestionPaper(subject=subject, date_time=form.cleaned_data['date_time'], duration=form.cleaned_data['duration'], instructions=form.cleaned_data['instructions'], pass_mark=0, max_marks=0)
            newQPaper.save()
            return HttpResponseRedirect(reverse('view_subject', args=[subject.subject_code]))
    else:
        form=CreateTestForm(initial={'date_time':datetime.datetime.today(), 'duration':datetime.timedelta(minutes=60)})
    return render(request, 'create_test.html', context={'form':form})