from rest_framework import permissions


class IsPortfolioOwnerOrEditorOrReadOnly(permissions.BasePermission):
    """
    Role-based permission for Portfolio API:
    - Visitor (Unauthenticated): Read-only (GET, HEAD, OPTIONS).
    - Regular User: Read-only for general endpoints (Star action handled separately).
    - Editor: Read + Modify (PUT, PATCH), cannot create (POST) or delete (DELETE).
    - Portfolio Owner (Superuser): Full access (Create, Read, Update, Delete).
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not (request.user and request.user.is_authenticated):
            return False

        if request.user.is_superuser:
            return True

        is_editor = request.user.groups.filter(name='Editor').exists()
        if is_editor and request.method in ['PUT', 'PATCH']:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not (request.user and request.user.is_authenticated):
            return False

        if request.user.is_superuser:
            return True

        is_editor = request.user.groups.filter(name='Editor').exists()
        if is_editor and request.method in ['PUT', 'PATCH']:
            return True

        return False


class IsPortfolioOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow portfolio owners (superuser) to edit or delete,
    while allowing read-only access for others.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)

