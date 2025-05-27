from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Attendance
from departments.models import Department
from users.models import UserProfile


class AttendanceTestCase(APITestCase):

    def setUp(self):
        # Create a department
        self.department = Department.objects.create(name='Department')

        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            department=self.department,
            role='EMPLOYEE',
            position='Secretary',
            phone='123456',
            address='Test Address'
        )
        self.client.force_authenticate(user=self.user)
        self.clock_in_url = '/attendance/clock_in/'
        self.clock_out_url = '/attendance/clock_out/'

    def test_clock_in_success(self):
        response = self.client.post(self.clock_in_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        attendance = Attendance.objects.get(employee=self.user, date=timezone.localtime(timezone.now()).date())
        self.assertIsNotNone(attendance.clock_in_time)
        self.assertEqual(attendance.status, 'Present')

    def test_clock_in_twice_same_day(self):
        # First clock in
        self.client.post(self.clock_in_url)
        # Second clock in should fail
        response = self.client.post(self.clock_in_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'You already clocked in')

    def test_clock_out_without_clock_in(self):
        response = self.client.post(self.clock_out_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'You must clock in first')

    def test_clock_out_success(self):
        # Clock in first
        self.client.post(self.clock_in_url)

        # Fast-forward time a bit (simulate clock-out after clock-in)
        attendance = Attendance.objects.get(employee=self.user, date=timezone.localtime(timezone.now()).date())
        attendance.clock_in_time = timezone.localtime(timezone.now()).replace(hour=8, minute=0, second=0).time()
        attendance.save()

        response = self.client.post(self.clock_out_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        updated = Attendance.objects.get(id=attendance.id)
        self.assertIsNotNone(updated.clock_out_time)

    def test_clock_out_twice(self):
        self.client.post(self.clock_in_url)
        attendance = Attendance.objects.get(employee=self.user, date=timezone.localtime(timezone.now()).date())
        attendance.clock_in_time = timezone.localtime(timezone.now()).replace(hour=8, minute=0).time()
        attendance.clock_out_time = timezone.localtime(timezone.now()).replace(hour=17, minute=0).time()
        attendance.save()

        response = self.client.post(self.clock_out_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'You already clocked out')

    def test_clock_out_before_clock_in_invalid(self):
        self.client.post(self.clock_in_url)
        attendance = Attendance.objects.get(employee=self.user, date=timezone.localtime(timezone.now()).date())

        # Force invalid time
        attendance.clock_in_time = timezone.localtime(timezone.now()).replace(hour=18, minute=0).time()
        attendance.save()

        response = self.client.post(self.clock_out_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Clock-out must be after clock-in.')
