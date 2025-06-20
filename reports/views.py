from rest_framework.views import APIView
from django.contrib.auth.models import User
from attendance.models import Attendance
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import date, datetime
from calendar import monthrange
from leave_request.models import LeaveRequest
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.timezone import now

from users.models import UserProfile


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


    date_param = openapi.Parameter(
        "date", openapi.IN_QUERY, description="Date in YYYY-MM-DD format", type=openapi.TYPE_STRING, required=False
    )

    @swagger_auto_schema(manual_parameters=[date_param])
    def get(self, request):
        current_date = now().strftime("%Y-%m-%d")
        today = request.query_params.get('date', current_date)
        report = []

        users = User.objects.all()
        for user in users:
            attendance = Attendance.objects.filter(employee=user, date=today).first()
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
    Query param: ?month=YYYY-MM&user_id=1

    For each date, it returns
        - Date
        - Clock in time
        - Clock out time
        - status
    """

    permission_classes = [IsAuthenticated]

    user_param = openapi.Parameter(
        "user_id", openapi.IN_QUERY, description="User ID", type=openapi.TYPE_INTEGER, required=True
    )
    month_param = openapi.Parameter(
        "month", openapi.IN_QUERY, description="Month in YYYY-MM format", type=openapi.TYPE_STRING, required=False
    )

    @swagger_auto_schema(manual_parameters=[month_param, user_param])
    def get(self, request):

        current_month = now().strftime("%Y-%m")
        month_str = request.query_params.get('month', current_month)
        user_id = request.query_params.get("user_id")

        if not month_str:
            month_str = datetime.now().strftime('%Y-%m')

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


class EmployeeLeaveHistoryReport(APIView):
    """
    API endpoint to retrieve the leave history for a specific employee.

    Query Parameters:
        - user_id (int): User ID of the employee whose leave history is to be retrieved.

    Returns a list of leave records with the following details:
        - Date of request creation
        - Leave start date
        - Leave end date
        - Status of the leave (Pending, Approved, Rejected)
        - Reviewed timestamp
        - Name of the reviewer (if available)
    """

    permission_classes = [IsAuthenticated]

    employee_param = openapi.Parameter(
        "user_id", openapi.IN_QUERY, description="User ID", type=openapi.TYPE_INTEGER, required=True
    )

    @swagger_auto_schema(manual_parameters=[employee_param])
    def get(self, request):
        user_id = request.query_params.get("user_id")

        leave_history = LeaveRequest.objects.filter(
            employee_id = user_id
        )

        data = []

        for history in leave_history:
            data.append({
                "date":history.created_at,
                "start_date":history.start_date,
                "end_date": history.end_date,
                "status":history.status,
                "reviewed_at":history.reviewed_at,
                "reviewed_by":history.reviewed_by.get_full_name() if history.reviewed_by else None
            })

        return Response(data)


class EmployeeLeaveBalanceReport(APIView):
    """
    API endpoint to retrieve the leave balance for a specific employee.
    Query Parameters:
    - user_id (int): user ID of the employee whose leave balance is to be retrieved.
    Returns the leave balance of an employee.:
    """

    permission_classes = [IsAuthenticated]

    user_id_param = openapi.Parameter(
        "user_id", openapi.IN_QUERY, description='USER ID', type=openapi.TYPE_INTEGER, required=True
    )

    @swagger_auto_schema(manual_parameters=[user_id_param])
    def get(self, request):
        user_id = request.query_params.get("user_id")

        employee = UserProfile.objects.filter(user_id=user_id).first()

        return Response({"leave_balance": employee.leave_balance})
