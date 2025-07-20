

# Create your models here.
from cloudinary.models import CloudinaryField
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
# from auth_api.models import *
from django.contrib.auth.models import Group, Permission

# Create your models here.
class TeacherManager(BaseUserManager):
    def create_user(self, email, full_name, password=None,password2=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, full_name, password, **extra_fields)

class Teacher(AbstractBaseUser, PermissionsMixin):
    groups = models.ManyToManyField(
        Group,
        related_name='teacher_set',
        blank=True,
        help_text='Groups for the teacher',
        related_query_name='teacher',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='teacher_permissions',
        blank=True,
        help_text='Permissions for the teacher',
        related_query_name='teacher',
    )
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    qualification = models.CharField(max_length=100)
    mobilenumber = models.CharField(max_length=100)
    address = models.TextField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = TeacherManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin



