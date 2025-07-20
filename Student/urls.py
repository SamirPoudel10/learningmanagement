"""
URL configuration for lms_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from .views import *


urlpatterns = [
    path('register/', user_registration.as_view(),name='register'),
    path('login/', user_login.as_view(),name='login'),
    path('profile/',user_profile.as_view(),name='profile'),
    path('change-password/',ChangePassword.as_view(),name='change-password'),
    path('sendreset-password/',sendresetpass.as_view(),name='sendreset-password'),
    path('reset/<uid>/<token>/',userpassreset.as_view(),name='reset-password'),
    

    # path('assignment/',AssignmentView.as_view(),name='assignment'),
    path('logout/', LogoutView.as_view(), name='api_logout'),
]

