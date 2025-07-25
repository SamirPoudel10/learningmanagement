

# Create your models here.
from cloudinary.models import CloudinaryField
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
# from auth_api.models import *
from django.contrib.auth.models import Group, Permission
from user.models import *


class StudentManager(BaseUserManager):
    def create_student(self,user, **extra_fields):
        if not user:
            raise ValueError("user is required")
        
        user = self.model(user=user, **extra_fields)
        user.save(using=self._db)
        return user
class Student(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='student_user')
    interested_categories=models.CharField(max_length=250,blank=True,null=True)
    objects=StudentManager()
# Create your models here.
    def __str__(self):
        return self.user.email
