from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """
    Custom permission to only allow access to Admin users.
    """
    def has_permission(self, request, view):
        return request.user_authenticated and request.user.role == 'ADMIN'

class IsLandlord(BasePermission):
    """
    Custom permission to only allow access to Landlord users.
    """
    def has_permission(self, request, view):
        return request.user_authenticated and request.user.role == 'LANDLORD'

class IsTenant(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'TENANT'

