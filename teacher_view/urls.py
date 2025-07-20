from django.urls import path
from . import views
urlpatterns=[
   
    path('dashboard/',views.dashboard,name='teacher_dashboard'),
    path('course/',views.course,name='teacher_course'),
    path('student/',views.student,name='teacher_student'),
    path('course/add/',views.course_add,name='course_add'),
    path('category/add/',views.category_add,name='category_add')
    
    
]