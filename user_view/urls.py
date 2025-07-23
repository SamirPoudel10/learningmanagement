from django.urls import path
from . import views
urlpatterns=[
    path('',views.home,name='home'),
    path('login/',views.login_page,name='login_page'),
    path('signup/',views.signup,name='signup_page'),
    path('about-us/',views.about_us,name="about_us"),
    path('contact-us/',views.contact_us,name="contact_us"),
    path('login_response',views.login_response,name='login_response'),
    path('signup_response',views.signup_response,name='signup_response'),    
]