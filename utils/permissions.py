from rest_framework.permissions import BasePermission, SAFE_METHODS


class ReadOnlyOrAdminEdit(BasePermission):
    """
    - Everyone can read (GET).
    - Only ADMIN, HR, or MANAGER can edit (POST/PUT/PATCH/DELETE).
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        profile = getattr(request.user, 'userprofile', None)
        return (
            request.user.is_authenticated and
            profile and profile.role in ['ADMIN', 'HR', 'MANAGER']
        )