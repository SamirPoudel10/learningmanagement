from django.shortcuts import render
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from .serializers import *
from django.contrib.auth import authenticate,login
from course.models import *
from course.serializers import *
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from rest_framework import generics
from.models import *

class Courselist(APIView):
    def get(self,request,format=None):
        course=Course.objects.filter(teacher=1)
        serialiser=CourseSerializer(course,many=True)
        # if serialiser.is_valid():
        # serialiser.json()
        print(serialiser)
        return Response({'courses': serialiser.data}, status=status.HTTP_200_OK)
class Studentlist(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        teacher=1

        courses = Course.objects.filter(teacher=teacher)
        print(courses)

        all_enrollments = []
        for course in courses:
            print(course.id)
            enrollments = Student_enrollment.objects.filter(course=course.id)
            serializer = EnrollmentSerializer(enrollments, many=True)
            all_enrollments.extend(serializer.data)  # accumulate serialized data
        print(all_enrollments)
        return Response({'courses': all_enrollments}, status=status.HTTP_200_OK)
