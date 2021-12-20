from rest_framework import permissions

class IsClientOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):

        # Give read only permissions to all
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Client flag based permission
        return request.user.is_client == True


class IsVendor(permissions.BasePermission):

    def has_permission(self, request, view):

        # Vendor flag based permission
        return request.user.is_vendor == True

class IsClient(permissions.BasePermission):

    def has_permission(self, request, view):

        # Client flag based permission
        return request.user.is_client == True
