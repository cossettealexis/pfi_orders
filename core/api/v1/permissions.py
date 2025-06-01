from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsRoleAdmin(BasePermission):
    """
    Allows access only to users with role 'ADMIN'.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'role', None) == 'ADMIN'

class IsAdminOrReadOnly(BasePermission):
    """
    Allows authenticated users to perform safe (read-only) methods.
    Only users with role 'ADMIN' can perform write operations (POST, PUT, PATCH, DELETE).
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and getattr(request.user, 'role', None) == 'ADMIN'