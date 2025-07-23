from rest_framework import permissions
from Teacher.models import Teacher
from Student.models import Student

class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        print(request.user)
        return request.user and request.user.role=='teacher'
class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role=='student'