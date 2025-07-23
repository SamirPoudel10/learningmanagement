from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Student)
# @admin.register(Student)
# class StudentAdmin(admin.ModelAdmin):
#     list_display = ['user.email', 'full_name', 'is_staff']   
#     fieldsets=[('Credential',{'fields':('email','password')}),
#     ('Personal_info',{'fields':('full_name','mobilenumber','address','qualification','interested_categories')}),
#     ]
#     search_fields=[
#     'email'
#     ]

