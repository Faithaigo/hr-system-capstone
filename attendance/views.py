from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Attendance
from .serializers import AttendanceSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone


class AttendanceViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for attendance records.

    Custom actions:
    - clock_in: Marks the start of work for the current logged in employee.
    - clock_out: Marks the end of work, only if user already clocked in.
    """

    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def clock_in(self, request):
        """
        Allows the currently logged-in employee to clock in for today.
        Prevents multiple clock-ins on the same day.
        """
        user = request.user
        today = timezone.localtime(timezone.now()).date()
        attendance, created = Attendance.objects.get_or_create(employee=user, date=today)

        if attendance.clock_in_time:
            return Response({"detail": "You already clocked in"}, status=400)

        attendance.clock_in_time = timezone.localtime(timezone.now()).time()
        attendance.status = 'Present'
        attendance.save()
        return Response({"detail": "You've clocked in successfully"}, status=201)

    @action(detail=False, methods=['post'])
    def clock_out(self, request):
        """
        Allows the currently logged-in employee to clock out for today.
        Only allowed if clock-in already happened and clock-out is after it.
        """
        user = request.user
        today = timezone.localtime(timezone.now()).date()

        attendance = Attendance.objects.filter(employee=user, date=today).first()
        if not attendance:
            return Response({"detail": "You must clock in first"}, status=400)

        if not attendance.clock_in_time:
            return Response({"detail": "You must clock in first"}, status=400)
        if attendance.clock_out_time:
            return Response({"detail": "You already clocked out"}, status=400)

        now = timezone.localtime(timezone.now()).time()

        if now <= attendance.clock_in_time:
            return Response({"detail": "Clock-out must be after clock-in."}, status=400)

        attendance.clock_out_time = now
        attendance.save()
        return Response({"detail": "You've clocked out successfully"}, status=201)
