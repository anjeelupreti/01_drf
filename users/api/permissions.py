from rest_framework import permissions

class IsSuperAdmin(permissions.BasePermission):
    """
    Allows access only to Super Admin users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_super_admin)

class IsCountryAdmin(permissions.BasePermission):
    """
    Allows access only to Country Admin users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_country_admin)

class IsCountryAdminOrSuperAdmin(permissions.BasePermission):
    """
    Allows access to both Country Admin and Super Admin users.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            (request.user.is_super_admin or request.user.is_country_admin)
        )

class CanCreateUsersForCountry(permissions.BasePermission):
    """
    Custom permission to check if user can create users for specific country.
    This is used in conjunction with serializer validation.
    """
    def has_permission(self, request, view):
        # Basic authentication check
        return bool(request.user and request.user.is_authenticated)