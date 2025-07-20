from rest_framework import serializers
# from main.models import *
from .models import *


# later in code:
from cloudinary.utils import cloudinary_url


 
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model=Teacher
        fields='__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }
