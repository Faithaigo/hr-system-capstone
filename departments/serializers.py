from rest_framework import serializers
from .models import Department

class DepartmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'description']