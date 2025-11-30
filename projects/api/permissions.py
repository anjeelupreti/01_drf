from rest_framework import permissions

class CanAccessProject(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        
        if user.is_super_admin:
            return True
        elif user.is_country_admin or user.is_member:
            return obj.country == user.country
        
        return False

class CanCreateProject(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.method == 'POST':
            return True
        
        return True  

class CanEditProject(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        user = request.user
        if user.is_super_admin or user.is_country_admin:
            return True
        
        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if user.is_super_admin:
            return True
        elif user.is_country_admin:
            return obj.country == user.country
        elif user.is_member:
            return False
        
        return False

class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_super_admin)

class IsCountryAdminOrSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            (request.user.is_super_admin or request.user.is_country_admin)
        )

class CanViewProjectStatistics(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        user = request.user
        if user.is_super_admin or user.is_country_admin:
            return True
        
        return False