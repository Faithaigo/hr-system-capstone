from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User

from departments.models import Department
from .models import UserProfile
from auditlog.models import AuditLog


class EmployeeViewSetTests(APITestCase):

    def setUp(self):
        # Create a department
        self.department = Department.objects.create(name='Department')

        # Create a normal user and department
        self.user = User.objects.create_user(username='employee', password='test123')
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            department=self.department,
            role='EMPLOYEE',
            position='Secretary',
            phone='123456',
            address='Test Address'
        )

        # Create an admin user
        self.admin_user = User.objects.create_user(username='admin', password='admin123')
        self.admin_profile = UserProfile.objects.create(
            user=self.admin_user,
            role='ADMIN',
            department=self.department,
            position='Administrator',
            phone='7890',
            address='Admin Address'
        )

        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get('/employees/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_employees(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/employees/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_retrieve_employee(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(f'/employees/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['position'], 'Secretary')

    def test_create_employee_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        payload = {
            "user": {
                "username": "newuser",
                "password": "newpass",
                "first_name": "newfirstname",
                "last_name": "newlastname",
                "email": "newuser@gmail.com",
            },
            "role": "EMPLOYEE",
            "department": self.department.id,
            "position": "Developer",
            "phone": "5555",
            "address": "New Addr"
        }

        response = self.client.post('/employees/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(UserProfile.objects.filter(position='Developer').exists())
        self.assertTrue(AuditLog.objects.filter(action="Created newuser@gmail.com").exists())

    def test_update_employee_as_non_admin_forbidden(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            "position": "Updated Position"
        }
        response = self.client.patch(f'/employees/{self.user.id}/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_employee_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        payload = {
            "position": "Updated HR"
        }
        response = self.client.patch(f'/employees/{self.user_profile.id}/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['position'], "Updated HR")
        self.assertTrue(AuditLog.objects.filter(action__icontains='Updated').exists())
