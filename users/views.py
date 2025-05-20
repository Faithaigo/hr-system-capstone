from rest_framework.viewsets import ModelViewSet
from .models import UserProfile
from .serializers import UserProfileSerializer

class EmployeeViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
