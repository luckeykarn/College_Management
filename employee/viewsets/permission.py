from rest_framework.permissions import BasePermission  # permission base class
from rest_framework.exceptions import PermissionDenied  # optional for custom errors

class IsAdminOrHR(BasePermission):
    """
    Custom permission to allow only Admin or HR users to create employees.
    """
    message = "Only Admin or HR can create employees."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in ['Admin', 'HR']
        )
