from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.expressions import Case
from django.db.models.fields import CharField
from django.utils import tree
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Student(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    STUDENT_TYPES=(('FT', 'Full Time'), ('PT', 'Part Time'))
    student_type=models.CharField(max_length=2, choices=STUDENT_TYPES)

class Subject(models.Model):
    examiner=models.ForeignKey(User, on_delete=CASCADE)
    subject_code=models.CharField(max_length=10, unique=True)
    subject_name=models.CharField(max_length=50)

    def __str__(self):
        return self.subject_name

class Subjectregistered(models.Model):
    student = models.ForeignKey(Student, on_delete=CASCADE)
    subject = models.ForeignKey(Subject, on_delete=CASCADE)



class QuestionPaper(models.Model):
    subject=models.ForeignKey(Subject, on_delete=CASCADE)
    date_time=models.DateTimeField()
    duration=models.DurationField()
    instructions=models.TextField()
    pass_mark=models.FloatField()
    max_marks=models.FloatField()
    published=models.BooleanField(default=False)

class Question(models.Model):
    question_paper=models.ForeignKey(QuestionPaper, on_delete=CASCADE)
    question_text=models.TextField()
    assigned_marks=models.FloatField()
    awarded_marks=models.FloatField(default=0)

    def __str__(self):
        return self.question_text[:50]

class MCQ(models.Model):
    question=models.ForeignKey(Question, on_delete=CASCADE)
    options=ArrayField(models.CharField(max_length=100))
    correct_option=models.CharField(max_length=100)

class Test(models.Model):
    ''' Stores tests registered by student and total marks obtained for each. '''
    student=models.ForeignKey(Student, on_delete=CASCADE)
    question_paper=models.ForeignKey(QuestionPaper, on_delete=CASCADE)
    total_marks=models.FloatField(default=-1)

class StudentResponse(models.Model):
    ''' Stores response to each question by student. '''
    test=models.ForeignKey(Test, on_delete=CASCADE)
    question=models.ForeignKey(Question, on_delete=CASCADE)