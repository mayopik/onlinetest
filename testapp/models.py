from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.utils import tree

# Create your models here.

class Student(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    STUDENT_TYPES=(('FT', 'Full Time'), ('PT', 'Part Time'))
    student_type=models.CharField(max_length=2, choices=STUDENT_TYPES)