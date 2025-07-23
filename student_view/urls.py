from django.urls import path
from . import views
urlpatterns=[
    
    path('all_course/',views.course,name='course_page'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('my_course/',views.enrolledcourse,name='mycourse_page'),
    path('dashboard/',views.dashboard,name='student_dashboard'),
    path('assignment/',views.assignment,name='assignment'),
    path('cart/',views.cartview,name='cart'),
    path('add-to-cart/<int:course_id>/',views.addtocart,name='add-to-cart'),
    path('delete-cart/<int:course_id>/',views.deletecart,name='delete-cart'),
    path('logout_response',views.logout_response,name='logout_response'),
    path('view-content/<int:course_id>/',views.view_content,name='view-content')
    
]