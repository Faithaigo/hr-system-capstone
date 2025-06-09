from django.urls import path
from reports import views


urlpatterns = [
    path('attendance/daily', views.DailyTeamAttendanceReport.as_view()),
    path('attendance/monthly', views.MonthlyEmployeeAttendanceReport.as_view()),
    path('leave/history', views.EmployeeLeaveHistoryReport.as_view()),
    path('employee/leave_balance', views.EmployeeLeaveBalanceReport.as_view())
]