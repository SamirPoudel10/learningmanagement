from django.urls import path
from . import views
urlpatterns=[
   
    path('dashboard/',views.dashboard,name='teacher_dashboard'),
    path('course/',views.course,name='teacher_course'),
    path('student/',views.student,name='teacher_student'),
    path('course/add/',views.course_add,name='course_add'),
    path('course/delete/<int:course_id>/',views.course_delete,name='course_delete'),
    path('category/add/',views.category_add,name='category_add')
    
    
]