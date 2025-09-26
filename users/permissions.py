from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False


class IsPublic(BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.is_public:
            return True
        elif not obj.is_public and obj.user != request.user:
            return False
        else:
            return True
