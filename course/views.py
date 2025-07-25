from django.shortcuts import render
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from .serializers import *
from django.contrib.auth import authenticate,login
from .render import *
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from rest_framework import generics
from .models import *
from rest_framework.parsers import MultiPartParser, FormParser
from learningmanagementsystem.permissions import *
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

# Create your views here.

class CourseListView(APIView):
    permission_classes = [IsAuthenticated,IsStudent]

    def get(self, request, format=None):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CourseAddView(APIView):
    permission_classes=[IsAuthenticated,IsTeacher]
    parser_classes = (MultiPartParser, FormParser)
    def post(self,request,format=None):
        serializer_data=CourseAddSerializer(data=request.data)
        print(serializer_data)
        if serializer_data.is_valid(raise_exception=True):
            serializer_data.save()
            print("hi")
            return Response({'msg':'Course Added Successfully'},status=status.HTTP_201_CREATED) 
        print(serializer_data.errors)    
        return Response({'msg':'Course Addition Unsuccesful'},status=status.HTTP_404_NOT_FOUND)



class CategoryAddView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):
        serializer_data=CategoryAddSerializer(data=request.data)
        print(serializer_data)
        if serializer_data.is_valid(raise_exception=True):
            serializer_data.save()
            print("hi")
            return Response({'msg':'Course Added Successfully'},status=status.HTTP_201_CREATED) 
        print(serializer_data.errors)    
        return Response({'msg':'Course Addition Unsuccesful'},status=status.HTTP_404_NOT_FOUND)


class EnrolledCourseView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]  # No authentication needed for GET
        elif self.request.method == 'POST':
            return [IsTeacher()]  # Login required for POST
        return super().get_permissions()
    def get(self, request, format=None):
        user = request.user
        try:
            student = Student.objects.get(id=user.id)
            enrollments = Student_enrollment.objects.filter(student=student)
            print(enrollments)
            serializer = EnrollmentSerializer(enrollments, many=True)
            print(serializer.data)
            print("samir")
            return Response({'courses': serializer.data}, status=status.HTTP_200_OK)
            
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
class CourseDetailView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,course_id):
        user = request.user
        try:
            course = Course.objects.get(id=course_id)
            user=User.objects.get(id=user.id)
            student=Student.objects.get(user=user)
            cart=False
            enrolled=False
            if Cart.objects.filter(course=course,student=student).exists():
                cart=True
            if Student_enrollment.objects.filter(course=course,student=student).exists():
                enrolled=True
            serializer = CourseSerializer(course)

            return Response({'course': serializer.data,'cart':cart,'enrolled':enrolled}, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
 
class CartView(APIView):
    permission_classes = [IsAuthenticated,IsStudent]
        
    def post(self, request, format=None):
        try:
            user = request.user
            user=User.objects.get(id=user.id)
            student = Student.objects.get(user=user)
            course = Course.objects.get(id=request.data.get('course_id'))
            print(student,course)
            serializer = CartAddSerializer(data={
                'student': student.id,
                'course': course.id
            },context={
                'student': student,
                'course': course
            })
            print(serializer)
            if serializer.is_valid():
                print("hi")
                cart = serializer.save()
                return Response({'msg': 'Item added to Cart Successfully'}, status=status.HTTP_200_OK)
            else:
                print("Serializer errors:", serializer.errors)  
                print(serializer.errors)# <
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        # except Student.DoesNotExist:
        #     return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
    def get(self,request,format=None):
        try:
            user = request.user
            user=User.objects.get(id=user.id)
            student = Student.objects.get(user=user)
            cart_items = Cart.objects.filter(student=student)
            serializer = CartSerializer(cart_items, many=True)
            return Response({'cart': serializer.data}, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

            
    def delete(self,request,format=None):
        try:
            user=request.user
            user=User.objects.get(id=user.id)
            student=Student.objects.get(user=user)
            data=request.data
            course= Course.objects.get(id=data.get('course_id'))
            print(course)
            serializer = CartRemoveSerializer(data=request.data,context={
                'student': student,
                'course': course,
            })
            if serializer.is_valid():
                print()
                cart = serializer.remove(serializer)
                print(cart)
                cart=Cart.objects.filter(student=student)
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response({'error':'Cart NOt Found'},status=status.HTTP_404_NOT_FOUND)