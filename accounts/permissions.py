from rest_framework import permissions
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied

#  Custom permission to only allow authenticated users via JWT.
class IsAuthenticated(BasePermission): 
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

 
# Custom permission to check if user has specific role.Usage: permission_classes = [HasRole]
# Set required_role in the view class.
class HasRole(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        required_role = getattr(view, 'required_role', None)
        if not required_role:
            return True
        
        return request.user.has_role(required_role)


# Custom permission to check if user has specific permission.Usage: permission_classes = [HasPermission]
# Set required_permission in the view class.  
class HasPermission(BasePermission):
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        required_permission = getattr(view, 'required_permission', None)
        if not required_permission:
            return True
        
        return request.user.has_permission(required_permission)


# Custom permission to check if user can access resource with specific action.Usage: permission_classes = [CanAccessResource]
# Set required_resource and required_action in the view class.  
class CanAccessResource(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        required_resource = getattr(view, 'required_resource', None)
        required_action = getattr(view, 'required_action', None)
        
        if not required_resource or not required_action:
            return True
        
        return request.user.can_access(required_resource, required_action)

# Custom permission for Admin or HR roles only.  
class IsAdminOrHR(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        return request.user.has_role('admin') or request.user.has_role('hr')

# Custom permission for resource owner or HR role.
class IsOwnerOrHR(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # HR can access any object
        if request.user.has_role('hr') or request.user.has_role('admin'):
            return True
        
        # Check if user owns the object
        if hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'employee'):
            return obj.employee.user == request.user
        
        return False
    
# Admin can only create HR and employee
class IS_ADMIN(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Admin'
    
class IS_HR(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'HR'