from django.shortcuts import render,redirect
from rest_framework.authtoken.models import Token
import requests
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib import messages

from django.http import HttpResponseRedirect
def home(request):
    return render(request,'user_view/home.html')
def login_page(request):
    return render(request,'user_view/login.html')
def signup(request):
    return render(request,'user_view/signup.html')
def about_us(request):
    return render(request,'user_view/about.html')
def contact_us(request):
    return render(request,'user_view/contact.html')
def login_response(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        api_url = 'http://127.0.0.1:8000/api/user/login/'
        payload = {'email': email, 'password': password}
        headers = {'Content-Type': 'application/json'}

        api_response = requests.post(api_url, json=payload, headers=headers)

        if api_response.status_code in [200, 201]:
            data = api_response.json()

            # Extract tokens nested inside 'token' key
            tokens = data.get('token', {})

            access_token = tokens.get('access')
            refresh_token = tokens.get('refresh')
            role=data.get('role')
            print(role)

            if access_token and refresh_token:
                response=redirect('home')
                if role=='student':
                    response = redirect('student_dashboard')
                if role=='teacher':
                    response = redirect('teacher_dashboard')
                if role=='admin':
                    response=redirect('/admin/login/')

                # Set HttpOnly cookies
                response.set_cookie(
                    key='access_token',
                    value=access_token,
                    httponly=True,
                    samesite='Lax',
                    secure=False,  # Set True in production with HTTPS
                )
                response.set_cookie(
                    key='refresh_token',
                    value=refresh_token,
                    httponly=True,
                    samesite='Lax',
                    secure=False,
                )
                # login(request,request.user)
                messages.success(request, 'Login successful.')
                return response
            else:
                messages.error(request, 'Token missing in API response.')
        else:
            messages.error(request, 'Invalid credentials or API error.')

    return redirect('login_page')
def signup_response(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        full_name= f'{first_name} {last_name}'
        email = request.POST.get('email')
        qualification = request.POST.get('qualification')
        mobilenumber = request.POST.get('phone')
        address = request.POST.get('address')
        interested_categories = request.POST.get('interested_categories')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        print(password2)

        api_url = 'http://127.0.0.1:8000/api/user/register/'  # Your signup API URL

        payload = {
            'full_name': full_name,
            'email': email,
            'qualification': qualification,
            'mobilenumber': mobilenumber,
            'address': address,
            'interested_categories': interested_categories,
            'password': password,
            'password2': password2,
        }

        print(payload)  # Debugging
        headers = {'Content-Type': 'application/json'}
        response = requests.post(api_url, json=payload,headers = {'Content-Type': 'application/json'})
        print(response.status_code)

        if response.status_code == 201 :  # Usually 201 for successful creation
            messages.success(request, 'Signup successful. Please login.')
            return redirect('login_page')
        # else:
        #     error_data = response.json().get('errors', {})
        #     for field, errors in error_data.items():
        #         for error in errors:
        #             messages.error(request, f"{field.capitalize()}: {error}")
        #     print(response.text)  # Debugging error message

    return redirect('signup_page')
