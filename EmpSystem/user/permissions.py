from rest_framework.permissions import BasePermission
class IsAdmin(BasePermission):
     def has_object_permission(self, request, view):
          if request.user.role=='admin':
               return True
          else:
               return False