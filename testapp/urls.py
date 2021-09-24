from django.urls import path

from . import views

urlpatterns=[
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('registerStudent', views.registerStudent, name='register_student'),
    path('studentHome', views.studentHome, name='student_home'),
    path('examinerHome', views.examinerHome, name='examiner_home'),
    path('addSubject', views.addSubject, name='add_subject'),
]