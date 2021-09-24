from testapp.models import Student
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login

from testapp.forms import StudentRegistrationForm, RegistrationForm
# Create your views here.

def index(request):
    return render(request, 'index.html')

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

def studentHome(request):
    return HttpResponse('<h1>We have successfully registered you as a student.<h2>')

def examinerHome(request):
    return HttpResponse('<h1>We have successfully registered you as an examiner.<h2>')