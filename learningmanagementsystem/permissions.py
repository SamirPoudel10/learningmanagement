from rest_framework.permissions import BasePermission

class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and hasattr(request.user,Teacher)
