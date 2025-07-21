from rest_framework import permissions
from Teacher.models import Teacher
from Student.models import Student

class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and Teacher.objects.filter(email=request.user.email).exists()
class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and Student.objects.filter(email=request.user.email).exists()