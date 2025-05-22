from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Attendance(models.Model):
    """
    Represents the attendance record of an employee for a specific date.

    Fields:
        - employee: Reference to the User.
        - date: The date of attendance.
        - clock_in_time: Time the employee clocked in.
        - clock_out_time: Time the employee clocked out.
        - status: Attendance status (Present, Absent, On Leave).
    """
    employee = models.ForeignKey(User, related_name='attendances', on_delete=models.CASCADE)
    date = models.DateField(default=timezone.localtime(timezone.now()).date())
    clock_in_time = models.TimeField(null=True, blank=True)
    clock_out_time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=[('Present','Present'),('Absent','Absent'),('On Leave','On Leave')], default='Absent')

    class Meta:
        unique_together = ('employee','date') #an employee only has one record per day to avoid duplication
