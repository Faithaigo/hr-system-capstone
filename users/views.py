from rest_framework.viewsets import ModelViewSet
from .models import UserProfile
from .serializers import UserProfileSerializer
from utils.addLogs import add_audit_log
from rest_framework.permissions import IsAuthenticated
from utils.permissions import ReadOnlyOrAdminEdit

class EmployeeViewSet(ModelViewSet):
    """
    ViewSet for managing employee records (UserProfile).

    - Supports listing, retrieving, creating, and updating employee profiles.
    - Only authenticated users can access the endpoints.
    - Editing is restricted to users with ADMIN, HR, or MANAGER roles (see ReadOnlyOrAdminEdit permission).
    - Automatically logs actions (create/update) to the audit log.
    """

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, ReadOnlyOrAdminEdit]

    def perform_create(self, serializer):
        profile = serializer.save()
        add_audit_log(
            actor=self.request.user,
            action=f"Created {profile.user.email}",
            model="UserProfile",
            record_id=profile.id
        )

    def perform_update(self, serializer):
        profile = serializer.save()
        add_audit_log(
            actor=self.request.user,
            action=f"Updated {profile.user.email}",
            model="UserProfile",
            record_id=profile.id
        )