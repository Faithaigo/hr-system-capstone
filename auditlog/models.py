from django.db import models
from django.contrib.auth.models import User


class AuditLog(models.Model):
    """
    Model to store audit trail records for tracking changes or actions performed
    by users within the system.
    """
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=100)
    model = models.CharField(max_length=50)
    record_id = models.IntegerField()
    recorded_at = models.DateTimeField(auto_now_add=True)
