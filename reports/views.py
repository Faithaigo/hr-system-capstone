from rest_framework.views import APIView
from django.contrib.auth.models import User
from attendance.models import Attendance
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import date
from calendar import monthrange


class DailyTeamAttendanceReport(APIView):
    """
     API endpoint to retrieve today's attendance report for all employees.

     For each employee, it returns:
         - Employee name
         - Attendance data (Defaults to today if no attendance)
         - Clock-in time
         - Clock-out time
         - Attendance status (Present/Absent/On Leave)
     """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = request.query_params.get('date')
        report = []

        users = User.objects.all()
        for user in users:
            attendance = Attendance.objects.filter(employee=user, date=today).first()
            print(attendance)
            report.append({
                "employee":user.get_full_name(),
                "employee_id":user.id,
                "date": attendance.date if attendance else today,
                "time_in":attendance.clock_in_time if attendance else None,
                "time_out":attendance.clock_out_time if attendance else None,
                "status": attendance.status if attendance else "Absent"
            })

        return Response(report)


class MonthlyEmployeeAttendanceReport(APIView):
    """
    Returns attendance records for a single employee for a given month.
    Query param: ?month=YYYY-MM&employee_id=1

    For each date, it returns
        - Date
        - Clock in time
        - Clock out time
        - status
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        month_str = request.query_params.get('month')
        user_id = request.query_params.get("user_id")

        year = int(month_str.split('-')[0])
        month = int(month_str.split('-')[1])
        start_date = date(year, month, 1)
        end_date = date(year, month, monthrange(year,month)[1])

        attendance_records = Attendance.objects.filter(
            employee_id = user_id,
            date__range = [start_date, end_date]
        ).order_by('date')

        data = []

        for attendance in attendance_records:
            data.append({
                "date":attendance.date,
                "time_in":attendance.clock_in_time,
                "time_out": attendance.clock_out_time,
                "status":attendance.status
            })

        return Response(data)


