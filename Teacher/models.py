

# Create your models here.
from cloudinary.models import CloudinaryField
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
# from auth_api.models import *
from django.contrib.auth.models import Group, Permission
from user.models import *
class Teacher(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='teacher_user')
    def __str__(self):
        return self.user.email

   



