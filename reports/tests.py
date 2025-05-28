from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from django.utils import timezone
from datetime import date
from attendance.models import Attendance
from users.models import UserProfile
from departments.models import Department


class DailyTeamAttendanceReportTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.department = Department.objects.create(name='Department')


        self.user1 = User.objects.create_user(username='user1', password='pass1', first_name='User', last_name='One')
        self.user_profile1 = UserProfile.objects.create(
            user=self.user1,
            department=self.department,
            role='EMPLOYEE',
            position='Developer',
            phone='1234565657',
            address='Test Address1'
        )
        self.user2 = User.objects.create_user(username='user2', password='pass2', first_name='User', last_name='Two')

        self.user_profile2 = UserProfile.objects.create(
            user=self.user2,
            department=self.department,
            role='MANAGER',
            position='Manager',
            phone='1234569080',
            address='Test Address2'
        )
        self.client.force_authenticate(user=self.user1)

        # Attendance for user1
        Attendance.objects.create(
            employee=self.user1,
            date=date.today(),
            clock_in_time=timezone.now().time(),
            status='Present'
        )
        # No attendance for user2 to test Absent fallback

    def test_daily_team_attendance_report(self):
        response = self.client.get(f"/reports/attendance/daily?date={date.today()}")  # Update this to match your URL
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

        user1_report = None
        for item in response.data:
            if item["employee_id"] == self.user1.id:
                user1_report = item
                break
        self.assertEqual(user1_report["status"], "Present")

        user2_report = None
        for item in response.data:
            if item["employee_id"] == self.user2.id:
                user2_report = item
                break
        self.assertEqual(user2_report["status"], "Absent")

