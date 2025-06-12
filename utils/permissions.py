from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import UserProfile


class ReadOnlyOrAdminEdit(BasePermission):
    """
    - Everyone can read (GET).
    - Only ADMIN, HR, or MANAGER can edit (POST/PUT/PATCH/DELETE).
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        # Allow superusers always
        if request.user.is_superuser:
            return True

        profile = UserProfile.objects.filter(user=request.user).first()
        if request.user.is_authenticated and profile and profile.role in ["ADMIN", "HR", "MANAGER"]:
            return True