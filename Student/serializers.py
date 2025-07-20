from rest_framework import serializers
# from main.models import *
from .models import *
from .util import *  # correct import

# later in code:
from cloudinary.utils import cloudinary_url


 
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields='__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }
class StudentRegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'})
    class Meta:
        model=Student
        fields='__all__'
        extra_kwargs={
            'id': {'read_only': True},  
            'password':{'write_only':True}
        }
    def validate(self,data):
        password= data.get('password')
        password2=data.get('password2')
        if password != password2:
            raise serializers.ValidationError("Passwords doesnot match")

        return data
    def create(self,validate_data):
        return Student.objects.create_user(**validate_data)


class StudentLoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=Student
        fields=['email','password']
        
class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields='__all__'

class StudentChangePassSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def save(self, **kwargs):
        student = self.context.get('student')
        student.set_password(self.validated_data['password'])
        student.save()
        return student

class sendresetpassemailpassserialiser(serializers.Serializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        fields=['Email']
    def validate(self,attrs):
        email=attrs.get('email')
        if Student.objects.filter(email=email).exists():
            student=Student.objects.get(email=email)
            print(student)
            uid=urlsafe_base64_encode(force_bytes(student.id))
            print(uid)
            token=PasswordResetTokenGenerator().make_token(student)
            print(token)        
            link=f'http://localhost:8000/api/user/reset/{uid}/{token}'
            body="Click the link to reset your password " + link

            data={

                'subject':'Reset Your Password',
                'body':body,
                'to_email':student.email

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
            student=Student.objects.get(id=uid)
            if not PasswordResetTokenGenerator().check_token(student,token):
                raise serializers.ValidationError("Token isnot valid or expired")
            student.set_password(password)
            student.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator.check_token(user,token)
            raise serializers.ValidationError("Token isnot valid or expired")

    def save(self, **kwargs):
        student = self.context.get('student')
        student.set_password(self.validated_data['password'])
        student.save()
        return student


