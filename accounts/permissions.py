from rest_framework import permissions


# Custom permission to allow access only to students.
class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        Return True if the requesting user is a student.
        """
        if request.user.is_authenticated:
            return request.user.role == "user"
        return False


# Custom permission to allow access only to instructors.
class IsVendor(permissions.BasePermission):
    """
    Return True if the requesting user is an instructor.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == "vendor"
        return False


#  Custom permission to allow access only to admin users.
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        Return True if the requesting user is an admin.
        """
        if request.user.is_authenticated:
            return request.user.role == "admin"
        return False
