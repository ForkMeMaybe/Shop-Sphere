from rest_framework.permissions import (
    BasePermission,
    DjangoModelPermissions,
    SAFE_METHODS,
)
from rest_framework import permissions


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class FullDjangoModelPermissions(DjangoModelPermissions):
    def __init__(self) -> None:
        self.perms_map["GET"] = ["%(app_label)s.view_%(model_name)s"]


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in SAFE_METHODS:
            return True
        # Write permissions are only allowed to the owner of the review
        return obj.user == request.user
