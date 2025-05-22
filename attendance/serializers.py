from rest_framework import serializers
from .models import Attendance


class AttendanceSerializer(serializers.ModelSerializer):
    """
    Serializer for the Attendance model.

    Ensures that:
    - Clock-out cannot happen before or at the same time as clock-in.
    - Status, date, and employee are read-only to prevent tampering.
    """

    class Meta:
        model = Attendance
        fields = '__all__'
        read_only_fields = ['date','status','employee']

    def update(self, instance, validated_data):
        """
        Custom update method to validate that:
        - Clock-out time is only allowed if clock-in already exists.
        - Clock-out time must be after clock-in time.
        """
        if 'clock_out_time' in validated_data:
            if instance.clock_in_time is None:
                raise serializers.ValidationError("Cannot clock out without clocking in")
            if validated_data['clock_out_time'] <= instance.clock_in_time:
                raise serializers.ValidationError("Clock out time must be after clock in timee")
        return super().update(instance, validated_data)