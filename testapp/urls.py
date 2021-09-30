from django.urls import path

from . import views

urlpatterns=[
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('registerStudent', views.registerStudent, name='register_student'),
    path('studentHome', views.studentHome, name='student_home'),
    path('examinerHome', views.examinerHome, name='examiner_home'),
    path('addSubject', views.addSubject, name='add_subject'),
    path('subject/<str:sub_code>',views.viewSubject, name='view_subject'),
    path('createTest/<str:sub_code>', views.createTest, name='create_test'),
    path('editTest/<int:pk>', views.editTest, name='edit_test',),
    path('result/<int:pk>', views.result, name='result'),
    path('addMCQ/<int:test_id>', views.addMCQ, name='add_MCQ'),
    path('registernewsubject', views.registernewsubject, name='registernewsubject'),
]