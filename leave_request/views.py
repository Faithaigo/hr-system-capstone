from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import LeaveRequest
from .serializers import LeaveRequestSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime
from users.models import UserProfile
from utils.date_utils import calculate_difference


class LeaveRequestViewSet(ModelViewSet):
    """
    A viewset for handling leave request operations.

    Provides standard CRUD operations via the ModelViewSet base class.
    Includes custom actions to approve or reject leave requests.
    """

    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """
        Custom action to approve a leave request.

        This action:
        - Ensures the request is still pending before approving.
        - Updates the status to 'Approved'.
        - Records who reviewed the request and the timestamp.

        Args:
            request: The HTTP request object.
            pk: The primary key of the LeaveRequest to approve.

        Returns:
            Response: JSON response indicating success or failure.
        """
        try:
            leave = LeaveRequest.objects.get(pk=pk)

            if leave.status == 'Approved':
                return Response({'detail': 'This leave has already been approved'}, status=400)
            elif leave.status != 'Pending':
                return Response({'detail': 'Only pending requests can be approved'}, status=400)
            leave.status = 'Approved'
            leave.reviewed_by = request.user
            leave.reviewed_at = datetime.now()
            leave.save()

            employee_leave = LeaveRequest.objects.filter(employee_id=leave.employee_id).all()

            annual_leave_days = 21
            no_days = 0

            for request in employee_leave:
                days = calculate_difference(request.start_date, request.end_date)
                no_days += days

            leave_balance = annual_leave_days - no_days

            employee = UserProfile.objects.filter(user_id=leave.employee_id).first()
            employee.leave_balance = leave_balance
            employee.save()

            return Response({'message': 'Leave approved successfully'})

        except LeaveRequest.DoesNotExist:
            return Response({'detail': 'Leave request not found'}, status=404)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """
        Custom action to reject a leave request.

        This action:
        - Ensures the request is still pending before rejecting.
        - Updates the status to 'Rejected'.
        - Records who reviewed the request and the timestamp.

        Args:
            request: The HTTP request object.
            pk: The primary key of the LeaveRequest to reject.

        Returns:
            Response: JSON response indicating success or failure.
        """
        try:
            leave = LeaveRequest.objects.get(pk=pk)

            if leave.status != 'Pending':
                return Response({'detail': 'Only pending requests can be rejected'}, status=400)
            leave.status = 'Rejected'
            leave.reviewed_by = request.user
            leave.reviewed_at = datetime.now()
            leave.save()

            return Response({'message': 'Leave rejected'})

        except LeaveRequest.DoesNotExist:
            return Response({'detail': 'Leave request not found'}, status=404)
