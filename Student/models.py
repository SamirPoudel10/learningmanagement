

# Create your models here.
from cloudinary.models import CloudinaryField
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
# from auth_api.models import *
from django.contrib.auth.models import Group, Permission

class StudentManager(BaseUserManager):
    def create_user(self, email, full_name, password=None,password2=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(email, full_name, password, **extra_fields)




class Student(AbstractBaseUser, PermissionsMixin):
    groups = models.ManyToManyField(
        Group,
        related_name='student_set',
        blank=True,
        help_text='Groups for the student',
        related_query_name='student',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='student_permissions',
        blank=True,
        help_text='Permissions for the student',
        related_query_name='student',
    )
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    qualification = models.CharField(max_length=100)
    mobilenumber = models.CharField(max_length=100)
    address = models.TextField()
    interested_categories = models.TextField()
    is_active = models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    objects = StudentManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email







# Create your models here.
