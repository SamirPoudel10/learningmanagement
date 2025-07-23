from django.shortcuts import render,redirect
from rest_framework.authtoken.models import Token
import requests
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib import messages

from django.http import HttpResponseRedirect

# Create your views here.

def course(request):
    api_url = 'http://127.0.0.1:8000/api/course/' 
    access_token = request.COOKIES.get('access_token') 
    print(access_token) # Use access token
    if not access_token:
        print("hi")
        return render(request, 'course.html', {'courses': [], 'error': 'Access token missing'})
     
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(api_url,headers=headers)
    api_url2 = 'http://127.0.0.1:8000/api/course/cart/'
    response2 = requests.get(api_url2,headers=headers)
    if response.status_code == 200 :
        courses = response.json()
        print("hi")
    elif response.status_code == 401:  # Unauthorized, token expired
        # Here you can try to refresh token using refresh_token
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            # Call refresh token API to get new access token
            refresh_api_url = 'http://127.0.0.1:8000/api/token/refresh/'  # Your refresh endpoint
            refresh_response = requests.post(refresh_api_url, json={'refresh': refresh_token})
            if refresh_response.status_code == 200:
                new_access_token = refresh_response.json().get('access')
                if new_access_token:
                    # Set new access token cookie
                    response = redirect('enrolledcourse')  # reload this view
                    response.set_cookie('access_token', new_access_token, httponly=True, samesite='Lax', secure=False)
                    return response
            # If refresh fails, redirect to login
            return redirect('login_page')
        else:
            return redirect('login_page')

    else:
        courses = []
    print(response,response2)
    if response2.status_code == 200 :
        cart=response2.json()
    elif response.status_code == 401:  # Unauthorized, token expired
        # Here you can try to refresh token using refresh_token
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            # Call refresh token API to get new access token
            refresh_api_url = 'http://127.0.0.1:8000/api/token/refresh/'  # Your refresh endpoint
            refresh_response = requests.post(refresh_api_url, json={'refresh': refresh_token})
            if refresh_response.status_code == 200:
                new_access_token = refresh_response.json().get('access')
                if new_access_token:
                    # Set new access token cookie
                    response = redirect('enrolledcourse')  # reload this view
                    response.set_cookie('access_token', new_access_token, httponly=True, samesite='Lax', secure=False)
                    return response
            # If refresh fails, redirect to login
            return redirect('login_page')
        else:
            return redirect('login_page')
    
    else:
        cart = []
    context={'cart':cart,'courses':courses}
    print(context)
    return render(request,'student_view/course.html',context)
def dashboard(request):
    return render(request,'student_view/dashboard.html')

def logout_response(request):
    access_token = request.COOKIES.get('access_token') 
    print(access_token) # Use access token
    if not access_token:
        print("hi")
        return redirect('home')
    api_url = 'http://127.0.0.1:8000/api/user/logout/'
    headers = {'Authorization': f'Bearer {access_token}'}  # Use Bearer prefix for JWT

    response = requests.post(api_url, headers=headers)
    print(response)
    if response.status_code == 205:
        messages.success(request,"Logged out successfully")
        return redirect('home')
    elif response.status_code == 401:  # Unauthorized, token expired
        # Here you can try to refresh token using refresh_token
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            # Call refresh token API to get new access token
            refresh_api_url = 'http://127.0.0.1:8000/api/token/refresh/'  # Your refresh endpoint
            refresh_response = requests.post(refresh_api_url, json={'refresh': refresh_token})
            if refresh_response.status_code == 200:
                new_access_token = refresh_response.json().get('access')
                if new_access_token:
                    # Set new access token cookie
                    response = redirect('enrolledcourse')  # reload this view
                    response.set_cookie('access_token', new_access_token, httponly=True, samesite='Lax', secure=False)
                    return response
            # If refresh fails, redirect to login
            return redirect('login_page')
        else:
            return redirect('login_page')

    else:
        messages.warning(request,"Error While logging out")
        return redirect('student_dashboard')

    

def enrolledcourse(request):
    access_token = request.COOKIES.get('access_token')  # Use access token
    if not access_token:
        return render(request, 'mycourse.html', {'courses': [], 'error': 'Access token missing'})

    api_url = 'http://127.0.0.1:8000/api/student/enrolled-course/'
    headers = {'Authorization': f'Bearer {access_token}'}  # Use Bearer prefix for JWT

    response = requests.get(api_url, headers=headers)
    api_url2 = 'http://127.0.0.1:8000/api/course/cart/'
    response2 = requests.get(api_url2,headers=headers)
    if response.status_code == 200:
        courses = response.json()
    elif response.status_code == 401:  # Unauthorized, token expired
        # Here you can try to refresh token using refresh_token
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            # Call refresh token API to get new access token
            refresh_api_url = 'http://127.0.0.1:8000/api/token/refresh/'  # Your refresh endpoint
            refresh_response = requests.post(refresh_api_url, json={'refresh': refresh_token})
            if refresh_response.status_code == 200:
                new_access_token = refresh_response.json().get('access')
                if new_access_token:
                    # Set new access token cookie
                    response = redirect('enrolledcourse')  # reload this view
                    response.set_cookie('access_token', new_access_token, httponly=True, samesite='Lax', secure=False)
                    return response
            # If refresh fails, redirect to login
            return redirect('login_page')
        else:
            return redirect('login_page')
    else:
        courses = {}
    print(courses)
    if response2.status_code == 200 :
        cart=response2.json()    
    else:
        cart = []
        print("hi")
    context = {
    'courses': courses,
    'cart': cart  # make sure cart is defined or set to None/[] if not
    }
    print(context)
    return render(request, 'student_view/mycourse.html',context)


def course_detail(request,course_id):
    access_token = request.COOKIES.get('access_token')  # Use access token
    if not access_token:
        return render(request, 'student_view/mycourse.html', {'courses': [], 'error': 'Access token missing'})
    user_id = request.session.get('user_id')

    api_url = f'http://127.0.0.1:8000/api/course/{course_id}'
    headers = {'Authorization': f'Bearer {access_token}'}  # Use Bearer prefix for JWT

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        context = response.json()
    
    elif response.status_code == 401:  # Unauthorized, token expired
        # Here you can try to refresh token using refresh_token
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            # Call refresh token API to get new access token
            refresh_api_url = 'http://127.0.0.1:8000/api/token/refresh/'  # Your refresh endpoint
            refresh_response = requests.post(refresh_api_url, json={'refresh': refresh_token})
            if refresh_response.status_code == 200:
                new_access_token = refresh_response.json().get('access')
                if new_access_token:
                    #    Set new access token cookie
                    response = redirect('enrolledcourse')  # reload this view
                    response.set_cookie('access_token', new_access_token, httponly=True, samesite='Lax', secure=False)
                    return response
            # If refresh fails, redirect to login
            return redirect('login_page')
        else:
            return redirect('login_page')
    else:
        context = {}

    return render(request, 'student_view/course_detail.html',context)

def addtocart(request,course_id):
    access_token = request.COOKIES.get('access_token')  # Use access token
    if not access_token:
        return render('home')
    print(course_id)
    payload={
        "course_id":course_id
    }
    api_url = f'http://127.0.0.1:8000/api/course/cart/'
    headers = {'Authorization': f'Bearer {access_token}'}  # Use Bearer prefix for JWT

    response = requests.post(api_url,json=payload, headers=headers)
 
    if response.status_code == 200:
     
        messages.success(request, 'Item added to cart successfully')
        print(messages)
    
    elif response.status_code == 401:  # Unauthorized, token expired
        # Here you can try to refresh token using refresh_token
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            # Call refresh token API to get new access token
            refresh_api_url = 'http://127.0.0.1:8000/api/token/refresh/'  # Your refresh endpoint
            refresh_response = requests.post(refresh_api_url, json={'refresh': refresh_token})
            if refresh_response.status_code == 200:
                new_access_token = refresh_response.json().get('access')
                if new_access_token:
                    # Set new access token cookie
                    response = redirect('enrolledcourse')  # reload this view
                    response.set_cookie('access_token', new_access_token, httponly=True, samesite='Lax', secure=False)
                    return response
            # If refresh fails, redirect to login
            return redirect('login_page')
        else:
            return redirect('login_page')
    else:
        print("hi")
        messages.error(request,"Fail to add item to cart. Already in cart") 
    return redirect('course_detail',course_id=course_id)
def deletecart(request,course_id):
    access_token = request.COOKIES.get('access_token')  # Use access token
    if not access_token:
        return render('home')
    print(course_id)
    payload={
        "course_id":course_id
    }
    api_url = f'http://127.0.0.1:8000/api/course/cart/'
    headers = {'Authorization': f'Bearer {access_token}'}  # Use Bearer prefix for JWT

    response = requests.delete(api_url,json=payload, headers=headers)

    if response.status_code == 200:
        messages.warning(request, 'Item deleted from  cart successfully')
        print(messages)
    
    elif response.status_code == 401:  # Unauthorized, token expired
        # Here you can try to refresh token using refresh_token
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            # Call refresh token API to get new access token
            refresh_api_url = 'http://127.0.0.1:8000/api/token/refresh/'  # Your refresh endpoint
            refresh_response = requests.post(refresh_api_url, json={'refresh': refresh_token})
            if refresh_response.status_code == 200:
                new_access_token = refresh_response.json().get('access')
                if new_access_token:
                    # Set new access token cookie
                    response = redirect('enrolledcourse')  # reload this view
                    response.set_cookie('access_token', new_access_token, httponly=True, samesite='Lax', secure=False)
                    return response
            # If refresh fails, redirect to login
            return redirect('login_page')
        else:
            return redirect('login_page')
    else:
        print("hi")
        messages.error(request,"Fail to add item to cart. Already in cart")
       
    return redirect('cart')


def cartview(request):
    access_token = request.COOKIES.get('access_token')  # Use access token
    if not access_token:
        return render('home')
    api_url = f'http://127.0.0.1:8000/api/course/cart/'
    headers = {'Authorization': f'Bearer {access_token}'}  # Use Bearer prefix for JWT

    response = requests.get(api_url,headers=headers)
 
    if response.status_code == 200:
        cart=response.json()
    elif response.status_code == 401:  # Unauthorized, token expired
        # Here you can try to refresh token using refresh_token
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            # Call refresh token API to get new access token
            refresh_api_url = 'http://127.0.0.1:8000/api/token/refresh/'  # Your refresh endpoint
            refresh_response = requests.post(refresh_api_url, json={'refresh': refresh_token})
            if refresh_response.status_code == 200:
                new_access_token = refresh_response.json().get('access')
                if new_access_token:
                    # Set new access token cookie
                    response = redirect('enrolledcourse')  # reload this view
                    response.set_cookie('access_token', new_access_token, httponly=True, samesite='Lax', secure=False)
                    return response
            # If refresh fails, redirect to login
            return redirect('login_page')
        else:
            return redirect('login_page')
    else:
        cart=[]

        
        message.error(request,"Fail to load item. Please refresh the page")
    total_sum = sum(
    item.get('course', {}).get('category', {}).get('price', 0)
    for item in cart.get('cart', [])
    )   
    subtotal=total_sum-0.13*total_sum
    Tax=0.13*total_sum
    print(total_sum)
    # signature = generate_esewa_signature(total_amount, transaction_uuid, product_code, secret_key)
    return render(request,"student_view/cart.html",context={'cart':cart.get('cart'),'total_sum':total_sum,'sub_total':subtotal,'Tax':Tax})


def assignment(request):
    access_token = request.COOKIES.get('access_token')  # Use access token
    if not access_token:
        return render('home')
    api_url = f'http://127.0.0.1:8000/api/student/assignment/'
    headers = {'Authorization': f'Bearer {access_token}'}  # Use Bearer prefix for JWT

    response = requests.get(api_url,headers=headers)
 
    if response.status_code == 200:
        assignment=response.json()
        print(assignment)
        return render(request,"student_view/assignment.html",assignment)
    elif response.status_code==204:

        messages.success(request,"No Assignment Assigned")
    elif response.status_code == 401:  # Unauthorized, token expired
        # Here you can try to refresh token using refresh_token
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            # Call refresh token API to get new access token
            refresh_api_url = 'http://127.0.0.1:8000/api/token/refresh/'  # Your refresh endpoint
            refresh_response = requests.post(refresh_api_url, json={'refresh': refresh_token})
            if refresh_response.status_code == 200:
                new_access_token = refresh_response.json().get('access')
                if new_access_token:
                    # Set new access token cookie
                    response = redirect('enrolledcourse')  # reload this view
                    response.set_cookie('access_token', new_access_token, httponly=True, samesite='Lax', secure=False)
                    return response
            # If refresh fails, redirect to login
            return redirect('login_page')
        else:
            return redirect('login_page')
    else:
        print("hi")
        messages.error(request,"Fail to load item. Please refresh the page")
    return render(request,"student_view/assignment.html")
def view_content(request,course_id):
    access_token = request.COOKIES.get('access_token')  # Use access token
    if not access_token:
        return render(request, 'mycourse.html', {'courses': [], 'error': 'Access token missing'})
    user_id = request.session.get('user_id')

    api_url = f'http://127.0.0.1:8000/api/student/course/{course_id}'
    headers = {'Authorization': f'Bearer {access_token}'}  # Use Bearer prefix for JWT

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        content = response.json()
    
    elif response.status_code == 401:  # Unauthorized, token expired
        # Here you can try to refresh token using refresh_token
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            # Call refresh token API to get new access token
            refresh_api_url = 'http://127.0.0.1:8000/api/token/refresh/'  # Your refresh endpoint
            refresh_response = requests.post(refresh_api_url, json={'refresh': refresh_token})
            if refresh_response.status_code == 200:
                new_access_token = refresh_response.json().get('access')
                if new_access_token:
                    # Set new access token cookie
                    response = redirect('enrolledcourse')  # reload this view
                    response.set_cookie('access_token', new_access_token, httponly=True, samesite='Lax', secure=False)
                    return response
            # If refresh fails, redirect to login
            return redirect('login_page')
        else:
            return redirect('login_page')
    else:
        content = {}

    s=content.get('enrolled')
    print(s)
    first_video = None
    if content["course"]["topics"] and content["course"]["topics"][0]["videos"]:
        first_video = content["course"]["topics"][0]["videos"][0]
    else:
        first_video = None

    
    context = {
    "first_video": first_video,
    "content":content
    }
    print(context)
    print(context)
    if content.get('enrolled')==True:
        return render(request, 'viewcontent.html',context)
    else:
        messages.error(request,"You are not enrolled to this course")
        return render(request,'student_view/viewcontent.html')

import hmac
import hashlib
import base64

def generate_esewa_signature(total_amount, transaction_uuid, product_code, secret_key):
    # Prepare the string to sign exactly in this format:
    data_to_sign = f"total_amount={total_amount},transaction_uuid={transaction_uuid},product_code={product_code}"
    
    # Create HMAC SHA256 hash using the secret key
    signature = hmac.new(
        key=secret_key.encode('utf-8'),
        msg=data_to_sign.encode('utf-8'),
        digestmod=hashlib.sha256
    ).digest()

    # Encode the signature to base64 string
    signature_base64 = base64.b64encode(signature).decode()
    return signature_base64