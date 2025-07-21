from django.db import models

# Create your models here.


# Create your models here.
from cloudinary.models import CloudinaryField
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
# from auth_api.models import *
from django.contrib.auth.models import Group, Permission


class UserManager(BaseUserManager):
    def create_user(self, email, full_name, role,password=None,password2=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        if not role:
            raise ValueError("Role is required")
        email = self.normalize_email(email) 
        user = self.model(email=email, full_name=full_name,role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, full_name, password, **extra_fields)
class User(AbstractBaseUser,PermissionsMixin):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin','Admin')
    )
    
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    qualification = models.CharField(max_length=100)
    mobilenumber = models.CharField(max_length=100)
    address = models.TextField(null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
    role=models.CharField(max_length=10,choices=ROLE_CHOICES,default='student')
    def __str__(self):
        return self.email

