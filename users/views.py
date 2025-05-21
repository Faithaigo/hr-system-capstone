from rest_framework.viewsets import ModelViewSet
from .models import UserProfile
from .serializers import UserProfileSerializer
from utils.addLogs import add_audit_log
from rest_framework.permissions import IsAuthenticated

class EmployeeViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        employee = serializer.save()
        add_audit_log(
            actor=self.request.user,
            action=f"Created {employee.user.email}",
            model="UserProfile",
            record_id=employee.id
        )
