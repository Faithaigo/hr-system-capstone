from django.db import models
from django.contrib.auth.models import User
from departments.models import Department


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, related_name='department', on_delete=models.SET_NULL, null=True)
    role = models.CharField(max_length=15, choices=[('admin','ADMIN'),('manager','MANAGER'),('hr','HR'),('employee','EMPLOYEE')])
    position = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    leave_balance = models.IntegerField(default=0)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)



