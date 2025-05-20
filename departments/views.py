from rest_framework import viewsets
from .models import Department
from .serializers import DepartmentsSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    """
    This viewset provides functionality for creating, retrieving a list of departments, get single department,
    update and delete department
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentsSerializer