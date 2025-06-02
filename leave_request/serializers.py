from rest_framework import serializers
from .models import LeaveRequest
from users.models import UserProfile
from utils.date_utils import calculate_difference

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
        # employee = UserProfile.objects.filter(user=validated_data['employee']).first()

        leave_days =  calculate_difference(validated_data['start_date'], validated_data['end_date'])
        # if employee.leave_balance is not None:
        #     if leave_days > employee.leave_balance:
        #         raise serializers.ValidationError(f'You have only {employee.leave_balance} days left.')
        # else:
        if leave_days > 21:
            raise serializers.ValidationError('You can only take up to 21 days.')

        status = 'Pending'
        leave = LeaveRequest.objects.create(status=status, **validated_data)
        return leave