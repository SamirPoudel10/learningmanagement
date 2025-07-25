from django.shortcuts import render,redirect
from rest_framework.authtoken.models import Token
import requests
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib import messages
from .form import *
import json
from django.http import HttpResponseRedirect
from collections import defaultdict
# Create your views here.
def dashboard(request):
    return render(request,'teacher_view/dashboard.html')
def course(request):
    access_token = request.COOKIES.get('access_token')  # Use access token
    if not access_token:
        return render(request, 'teacher_view/course.html', {'courses': [], 'error': 'Access token missing'})

    api_url = 'http://127.0.0.1:8000/api/teacher/course'
    headers = {'Authorization': f'Bearer {access_token}'}  # Use Bearer prefix for JWT
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        courses = response.json()
    elif response.status_code == 401:  
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            refresh_api_url = 'http://127.0.0.1:8000/api/token/refresh/'
            refresh_response = requests.post(refresh_api_url, json={'refresh': refresh_token})
            if refresh_response.status_code == 200:
                new_access_token = refresh_response.json().get('access')
                if new_access_token:
                    response = redirect('enrolledcourse') 
                    response.set_cookie('access_token', new_access_token, httponly=True, samesite='Lax', secure=False)
                    return response
            return redirect('login_page')
        else:
            return redirect('login_page')
    elif response.status_code ==    403:
        return render(request,'permission_error.html')
    else:
        courses = {}
    
    print(courses)

    return render(request,'teacher_view/course.html',courses)

# def student(request):
    
def course_add(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        print("hi")
        if form.is_valid():
            print("hi")
            access_token = request.COOKIES.get('access_token')
            if not access_token:
                return render(request, 'student_view/mycourse.html', {
                    'courses': [], 
                    'error': 'Access token missing'
                })

            user_id = request.session.get('user_id')
            # Add user_id manually to form.cleaned_data or set in serializer backend
            category = form.cleaned_data['category']
            img = request.FILES['thumbnail']

            files = {
                'thumbnail': (img.name, img, img.content_type)
            }

            data = {
                'learning_outcomes': json.dumps(form.cleaned_data['learning_outcomes']),  # Ensure JSONField is serialized
                'category': str(category.id),
                'teacher': "1"  # must match DRF's expected input format (many-to-many requires ID list or single ID depending on setup)
            }

            api_url = 'http://127.0.0.1:8000/api/course/add/'
            headers = {'Authorization': f'Bearer {access_token}'}

            response = requests.post(api_url, data=data, files=files, headers=headers)
            print(response.status_code)
            if response.status_code == 201:
                return redirect('teacher_course')  # Successful creation

            elif response.status_code == 401:
                refresh_token = request.COOKIES.get('refresh_token')
                if refresh_token:
                    refresh_api_url = 'http://127.0.0.1:8000/api/token/refresh/'
                    refresh_response = requests.post(refresh_api_url, json={'refresh': refresh_token})
                    if refresh_response.status_code == 200:
                        new_access_token = refresh_response.json().get('access')
                        if new_access_token:
                            resp = redirect('course_add')
                            resp.set_cookie('access_token', new_access_token, httponly=True, samesite='Lax')
                            return resp
                    return redirect('login_page')
                else:
                    return redirect('login_page')
            else:
                return render(request, 'teacher_view/course_add.html', {
                    'form': form, 
                    'error': 'Something went wrong with the API.'
                })
        else:
            print(form.errors)
            return render(request, 'teacher_view/course_add.html', {'form': form})
    else:
        form = CourseForm()
    return render(request, 'teacher_view/course_add.html', {'form': form})
def category_add(request):
    if request.method == 'POST':
        form = CourseCategoryForm(request.POST)
        print("hi")
        if form.is_valid():
            print("hi")
            access_token = request.COOKIES.get('access_token')
            if not access_token:
                return render(request, 'teacher_view/course.html', {
                    'courses': [], 
                    'error': 'Access token missing'
                })
            title=form.cleaned_data['title']
            description=form.cleaned_data['description']
            duration=form.cleaned_data['duration']
            price=form.cleaned_data['price']
            data={
                'title':title,
                'description':description,
                'duration':duration,
                'price':price
            }
            api_url = 'http://127.0.0.1:8000/api/course/category/add/'
            headers = {'Authorization': f'Bearer {access_token}'}

            response = requests.post(api_url, data=data,  headers=headers)
            print(response.status_code)
            if response.status_code == 201:
                return render(request,'close_windows.html')  # Successful creation

            elif response.status_code == 401:
                refresh_token = request.COOKIES.get('refresh_token')
                if refresh_token:
                    refresh_api_url = 'http://127.0.0.1:8000/api/token/refresh/'
                    refresh_response = requests.post(refresh_api_url, json={'refresh': refresh_token})
                    if refresh_response.status_code == 200:
                        new_access_token = refresh_response.json().get('access')
                        if new_access_token:
                            resp = redirect('course_add')
                            resp.set_cookie('access_token', new_access_token, httponly=True, samesite='Lax')
                            return resp
                    return redirect('login_page')
                else:
                    return redirect('login_page')
            else:
                return render(request, 'teacher_view/course_add.html', {
                    'form': form, 
                    'error': 'Something went wrong with the API.'
                })
        else:
            print(form.errors)
            return render(request, 'teacher_view/course_add.html', {'form': form})
    else:
        form = CourseCategoryForm()
    return render(request, 'teacher_view/category_add.html', {'form': form})


def student(request):
    access_token = request.COOKIES.get('access_token')
    if not access_token:
        return render(request, 'teacher_view/student.html', {
            'courses': [], 
            'error': 'Access token missing'
        })
    api_url = 'http://127.0.0.1:8000/api/teacher/student/'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(api_url,  headers=headers)
    course=[]
    if response.status_code == 200:
        course=response.json()
        return render(request,'teacher_view/student.html',course)
    
    elif response.status_code == 401:
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            refresh_api_url = 'http://127.0.0.1:8000/api/token/refresh/'
            refresh_response = requests.post(refresh_api_url, json={'refresh': refresh_token})
            if refresh_response.status_code == 200:
                new_access_token = refresh_response.json().get('access')
                if new_access_token:
                    resp = redirect('course_add')
                    resp.set_cookie('access_token', new_access_token, httponly=True, samesite='Lax')
                    return resp
            return redirect('login_page')
        else:
            return redirect('login_page')
            
    else:
        grouped = defaultdict(list)
        for item in course:
            course_title = item["course"]["category"]["title"]
            grouped[course_title].append(item)
        print(grouped)
    return render(request, "teacher_view/student.html", {"grouped_students": dict(grouped)})
    