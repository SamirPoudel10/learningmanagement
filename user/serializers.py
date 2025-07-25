from rest_framework import serializers
from .models import *
from .util import *  

from cloudinary.utils import cloudinary_url

from Student.models import *
 
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }
class UserRegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'})
    class Meta:
        model=User
        fields='__all__'
        extra_kwargs={
            'id': {'read_only': True},  
            'password':{'write_only':True}
        }
    def validate(self,data):
        password= data.get('password')
        password2=data.get('password2')
        print("hi")
        if password != password2:
            raise serializers.ValidationError("Passwords doesnot match")

        return data
    def create(self,validate_data):
        user= User.objects.create_user(**validate_data,role='student')
        student=Student.objects.create_student(user=user)
        student.save()
        print(student)
        print("hi")
        print("HI")
        return user
        # return 


class UserLoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=User
        fields=['email','password']
        
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'

class UserChangePassSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def save(self, **kwargs):
        User = self.context.get('User')
        User.set_password(self.validated_data['password'])
        User.save()
        return User

class sendresetpassemailpassserialiser(serializers.Serializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        fields=['Email']
    def validate(self,attrs):
        email=attrs.get('email')
        if User.objects.filter(email=email).exists():
            User=User.objects.get(email=email)
            print(User)
            uid=urlsafe_base64_encode(force_bytes(User.id))
            print(uid)
            token=PasswordResetTokenGenerator().make_token(User)
            print(token)        
            link=f'http://localhost:8000/api/user/reset/{uid}/{token}'
            body="Click the link to reset your password " + link

            data={

                'subject':'Reset Your Password',
                'body':body,
                'to_email':User.email

            }
            Util.send_mail(data)  # correct usage

            print(link)
            return attrs
        else:
            raise ValidationError("You are not a Registered User")
        print(email)
        return email

class resetpass(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    def validate(self, attrs):
        try:

            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid=self.context.get('uid')
            token=self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("Passwords do not match.")
            uid=smart_str(urlsafe_base64_decode(uid))
            User=User.objects.get(id=uid)
            if not PasswordResetTokenGenerator().check_token(User,token):
                raise serializers.ValidationError("Token isnot valid or expired")
            User.set_password(password)
            User.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator.check_token(user,token)
            raise serializers.ValidationError("Token isnot valid or expired")

    def save(self, **kwargs):
        User = self.context.get('User')
        User.set_password(self.validated_data['password'])
        User.save()
        return User


