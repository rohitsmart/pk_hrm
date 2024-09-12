from rest_framework.permissions import BasePermission
class IsAdminOrHr(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.role=='hr' or request.user.role=='admin')
    
class IsAdminOrHrOrManager(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.role=='hr' or request.user.role=='admin'or request.user.role=='manager')