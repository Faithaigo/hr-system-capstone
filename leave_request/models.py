from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class LeaveRequest(models.Model):
    LEAVE_TYPES = [
        ('Annual Leave','Annual Leave'),
        ('Maternity Leave','Maternity Leave'),
        ('Bereavement','Bereavement'),
        ('Sick Leave','Sick Leave'),
        ('Parental Leave','Parental Leave'),
        ('Unpaid Leave','Unpaid Leave')
    ]
    leave_type = models.CharField(max_length=20,choices=LEAVE_TYPES, null=True)
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    custom_reason = models.TextField(null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=15, choices=[('Pending', 'Pending'),('Approved','Approved'),('Rejected','Rejected')])
    reviewed_by = models.ForeignKey(User, related_name='reviewed_leaves', on_delete=models.SET_NULL, null=True)
    reviewed_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
