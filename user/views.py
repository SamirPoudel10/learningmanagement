from django.shortcuts import render

# Create your views here.
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
from.models import *
from learningmanagementsystem.permissions import *

from rest_framework_simplejwt.tokens import RefreshToken, TokenError

# Create your views here.
def get_tokens_for_user(user):
    if not user.is_active:
      raise AuthenticationFailed("User is not active")

    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class user_registration(APIView):
    permission_classes = [AllowAny]
    renderer_classes=[User_renderer]
    def post(self,request,format=None):
        serializer_data=UserRegistrationSerializer(data=request.data)
        if serializer_data.is_valid(raise_exception=True):
            user=serializer_data.save()
            token=get_tokens_for_user(user)
            return Response({'token':token,'msg':'Registration successful'},status=status.HTTP_201_CREATED)     
        return Response({'msg':'Registration Unsuccesful'},status=status.HTTP_400_BAD_REQUEST)

class user_login(APIView):
    renderer_classes=[User_renderer]
    def post(self,request,format=None):
        print(request.data)
        serializer_data=UserLoginSerializer(data = request.data)
    
        if serializer_data.is_valid(raise_exception=True):
            email=serializer_data.data.get('email')
            password=serializer_data.data.get('password')
            user=authenticate(email=email,password=password)

            token=get_tokens_for_user(user)
            if user is not None:
                login(request,user)
                print(user.role)
                return Response({'token':token,'msg':'login successful','role':user.role},status=status.HTTP_201_CREATED)
                
            else:  
                return Response({'error':'login   unsuccessful'},status=status.HTTP_404_NOT_FOUND)
        return Response(serializers.errors,status=status.HTTP_404_NOT_FOUND)



class LogoutView(APIView):
    permission_classes = [IsAuthenticated,IsStudent]

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        access_token = request.COOKIES.get('access_token')
        print(refresh_token)
        try:
            refreshtoken=RefreshToken(refresh_token)
            refreshtoken.blacklist()
        except TokenError:
            return Response({'error': 'Token is invalid or expired.'}, status=status.HTTP_400_BAD_REQUEST)

        response = Response({'message': 'Successfully logged out.'}, status=status.HTTP_205_RESET_CONTENT)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response
class ChangePassword(APIView):
    renderer_classes = [User_renderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = StudentChangePassSerializer(data=request.data, context={'student': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Password changed successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class sendresetpass(APIView):
    renderer_classes=[User_renderer]
    def post(self,request,format=None):
        serializer= sendresetpassemailpassserialiser(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response ({'msg':'Password Reset link sent.Please Check Your Email'},status=status.HTTP_200_OK)
            
class userpassreset(APIView):
    renderer_classes=[User_renderer]
    def post(self,request,uid,token,format=None):
        serializer=resetpass(data=request.data,context={'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):
           
            return Response({'token':token,'msg':'Password reset done  successful'},status=status.HTTP_201_CREATED) 
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST) 

       


    
# class AssignmentView(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self,request,format=None):
#         try:
#             user=request.user
#             student=Student.objects.get(id=user.id)
#             assignment = Assignment.objects.filter(student=student)
#             serializer=AssignmentSerializer(assignment,many=True)
#             print("hi")
#             print(serializer.data)
#             return Response({'assignment': serializer.data}, status=status.HTTP_200_OK)
#         except:
#             return Response({'error':'Error Getting assignment'},status=status.HTTP_404_NOT_FOUND)










