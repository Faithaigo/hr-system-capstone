from django.db import models
from django.contrib.auth.models import User


class LeaveRequest(models.Model):
    """
    Model representing a leave request submitted by an employee.

    Tracks the type of leave, the employee requesting it, the time frame,
    and the status of the request (Pending, Approved, or Rejected).
    Also records who reviewed the request and when.
    """

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
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
