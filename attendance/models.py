from django.db import models
from django.contrib.auth.models import User


class Attendance(models.Model):
    employee = models.ForeignKey(User, related_name='employee', on_delete=models.CASCADE)
    date = models.DateField()
    clock_in_time = models.TimeField()
    clock_out_time = models.TimeField()
    status = models.CharField(max_length=15, choices=[('Present','Present'),('Absent','Absent'),('On Leave','On Leave')])
