from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsRoleAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'role', None) == 'ADMIN'

class IsAdminOrReadOnly(BasePermission):
    """
    Allows GET/HEAD/OPTIONS for everyone authenticated,
    but only allows POST/PUT/PATCH/DELETE for admin users.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and getattr(request.user, 'role', None) == 'ADMIN'