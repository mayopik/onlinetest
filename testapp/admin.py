from django.contrib import admin
from .models import MCQ, Question, QuestionPaper, Student, Subject

# Register your models here.

admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(QuestionPaper)
admin.site.register(Question)
admin.site.register(MCQ)