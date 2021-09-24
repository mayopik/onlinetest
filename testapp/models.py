from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
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
    subject_code=models.CharField(max_length=10, unique=True, primary_key=True)
    subject_name=models.CharField(max_length=50)

    def __str__(self):
        return self.subject_name

class Question(models.Model):
    subject=models.ForeignKey(Subject, on_delete=CASCADE)
    question_text=models.TextField()
    assigned_marks=models.FloatField()
    awarded_marks=models.FloatField()

class MCQ(models.Model):
    question=models.ForeignKey(Question, on_delete=CASCADE)
    options=ArrayField(models.CharField(max_length=100))
    correct_option=models.CharField(max_length=100)