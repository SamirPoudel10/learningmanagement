from django.contrib import admin
from django.urls import path,include
from .views import *


urlpatterns = [
    path('course/',Courselist.as_view(),name='api_teacher_course'),
    path('student/',Studentlist.as_view(),name='api_teacher_student')
]
