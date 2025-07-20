from django.urls import path
from .views import *
urlpatterns=[
    path('',CourseListView.as_view(),name='course'),
    path('add/',CourseAddView.as_view(),name='api_course_add'),
    path('category/add/',CategoryAddView.as_view(),name="api_category_add"),
    path('<int:course_id>/',CourseDetailView.as_view(),name='coursedetails'),
    path('enrolled/',EnrolledCourseView.as_view(),name='enrolled_course'),
    path('cart/',CartView.as_view(),name='cart_add'),
    
]