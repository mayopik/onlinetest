from typing import AsyncIterable
import datetime
from django.forms.models import model_to_dict

from django.http.response import Http404, HttpResponseBadRequest
from testapp.models import Student, Subject, QuestionPaper, Question, MCQ, Test
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import AddMCQForm, LoginForm, StudentRegistrationForm, RegistrationForm, AddSubjectForm, CreateTestForm, AddMCQForm

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

def registernewsubject(request):
    subs = Subject.objects.all()
    return render(request, 'subject_list.html', { 'subs':subs})

@login_required
def studentHome(request):
    context = {
        'fname' : request.user.first_name,
        'lname' : request.user.last_name,
        'last_login' : request.user.last_login,

    }
    return render(request, 'student_home.html', context)

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
    
    qpaper_list=QuestionPaper.objects.filter(subject=subject)
    
    return render(request, 'view_subject.html', context={'subject':subject, 'qpaper_list':qpaper_list})

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
            return HttpResponseRedirect(reverse('edit_test', args=[newQPaper.id]))
    else:
        form=CreateTestForm(initial={'date_time':datetime.datetime.today(), 'duration':datetime.timedelta(minutes=60)})
    return render(request, 'create_test.html', context={'form':form})

@login_required
def editTest(request, pk):
    try:
        qPaper=QuestionPaper.objects.get(id=pk)
    except QuestionPaper.DoesNotExist:
        raise Http404('Test does not exist!')
    
    context=dict()
    context['test']=qPaper
    context['question_list']=Question.objects.filter(question_paper=qPaper)

    return render(request, 'edit_test.html', context=context)

@login_required
def result(request, pk):
    try:
        res=Test.objects.get(id=pk)
    except Test.DoesNotExist:
        raise Http404('Subject is not available')

    context=dict()
    context['sub']=res.question_paper.subject
    context['total_marks']=res.total_marks

    if(context['total_marks'] >= res.question_paper.pass_mark):
         context['passed']=True

    context['per'] = (context['total_marks']/res.question_paper.max_marks)*100

    return render(request, 'result.html', context=context)


@login_required
def addMCQ(request, test_id):
    if request.method=="POST":
        data=request.POST.copy()
        #return HttpResponse(data.items())
        number_of_choices=int(data.pop('number_of_choices')[0])
        form=AddMCQForm(data, number_of_choices=number_of_choices)
        if form.is_valid():
            newQuestion=Question(question_paper=QuestionPaper.objects.get(id=test_id), question_text=form.cleaned_data['question_text'], assigned_marks=form.cleaned_data['assigned_marks'])
            newQuestion.save()
            newMCQ=MCQ(question=newQuestion, correct_option=form.cleaned_data['correct_option'], options=[])
            for i in range(number_of_choices):
                newMCQ.options.append(form.cleaned_data[f'option_{(i+1)}'])
            newMCQ.save()
            return HttpResponseRedirect(reverse('edit_test', args=[test_id]))
            # return HttpResponse(model_to_dict(newMCQ).items())
    else:
        try:
            if int(request.GET.get('n', '2'))<2:
                number_of_choices=2
            else:
                number_of_choices=int(request.GET.get('n', '2'))
        except:
            return HttpResponseBadRequest()
        form=AddMCQForm(number_of_choices=number_of_choices)
    
    return render(request, 'add_MCQ.html', context={'form':form})