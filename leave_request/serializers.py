from rest_framework import serializers
from .models import LeaveRequest


class LeaveRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and retrieving LeaveRequest objects.

    Ensures that when a leave request is created, its initial status is set to 'Pending'.
    All fields are included, but the 'status' field is read-only from the client side.
   """

    class Meta:
        model = LeaveRequest
        fields = '__all__'
        read_only_fields = ['status']

    def create(self, validated_data):
        status = 'Pending'

        leave = LeaveRequest.objects.create(status=status, **validated_data)
        return leave