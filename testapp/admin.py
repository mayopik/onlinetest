from django.contrib import admin
from .models import QuestionPaper, Student, Subject

# Register your models here.

admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(QuestionPaper)