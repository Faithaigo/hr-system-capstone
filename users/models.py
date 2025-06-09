from django.db import models
from django.contrib.auth.models import User
from departments.models import Department


class UserProfile(models.Model):
    """
    Extends the default Django User model with additional profile information
    such as department, role, position, contact details, and metadata.

    This model is linked to the built-in User model via a one-to-one relationship,
    allowing for custom fields specific to the employee.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, related_name='department', on_delete=models.SET_NULL, null=True)
    role = models.CharField(max_length=15, choices=[('ADMIN','ADMIN'),('MANAGER','MANAGER'),('HR','HR'),('EMPLOYEE','EMPLOYEE')])
    position = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    leave_balance = models.IntegerField(null=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)



