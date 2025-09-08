from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admins to edit it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Write permissions are only allowed to the owner or admin
        if hasattr(obj, 'user'):
            return obj.user == request.user or request.user.is_staff
        return obj == request.user or request.user.is_staff


class IsTeacherOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow teachers or admins to perform certain actions.
    """
    
    def has_permission(self, request, view):
        # Read permissions are allowed to any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Write permissions are only allowed to teachers or admins
        return request.user.user_type == 'teacher' or request.user.is_staff