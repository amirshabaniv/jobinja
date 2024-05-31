from rest_framework.permissions import BasePermission
    

class IsEmployer(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_employer


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.employer


class IsOwner2(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return request.user == obj.user