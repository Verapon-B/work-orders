from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import WorkOrder, OperationLog, Cleaning
from .serializers import WorkOrderSerializer
from .choices import UserRole, WorkOrderType, Action


class WorkOrderViewSet(viewsets.ModelViewSet):
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderSerializer

    def create(self, request, *args, **kwargs):
        work_order_type = request.data.get('work_order_type')
        user_role = request.user.role if request.user.is_authenticated else None

        if work_order_type == WorkOrderType.CLEANING:
            if user_role != UserRole.SUPERVISOR:
                return Response(
                    {'error': 'Only Maid Supervisor can create Cleaning work orders.'},
                    status=status.HTTP_403_FORBIDDEN
                )

        elif work_order_type in [WorkOrderType.MAID_REQUEST, WorkOrderType.TECHNICIAN_REQUEST]:
            if user_role != UserRole.SUPERVISOR:
                return Response(
                    {'error': 'Only Maid Supervisor can create Maid Request and Technician Request work orders.'},
                    status=status.HTTP_403_FORBIDDEN
                )

        elif work_order_type == WorkOrderType.AMENITY_REQUEST:
            if user_role != UserRole.GUEST:
                return Response(
                    {'error': 'Only guests can create Amenity Request work orders.'},
                    status=status.HTTP_403_FORBIDDEN
                )

        else:
            return Response({'error': 'Invalid work order type.'}, status=status.HTTP_400_BAD_REQUEST)

        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            log_entry = OperationLog.objects.create(
                user=request.user,
                action=Action.CREATE.value,
                model='WorkOrder',
                object_id=response.data['id'],
                details=f"Created by {request.user.username}"
            )

        return response

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user_role = request.user.role if request.user.is_authenticated else None

        if instance.work_order_type == WorkOrderType.CLEANING:
            if user_role == UserRole.SUPERVISOR:
                if request.data.get('cancel_by_guest'):
                    cleaning_instance = Cleaning.objects.get(work_order=instance)
                    cleaning_instance.cancel_by_guest = True
                    cleaning_instance.save()
            else:
                return Response(
                    {'error': 'Only Maid Supervisor can update Cleaning work orders.'},
                    status=status.HTTP_403_FORBIDDEN
                )

        response = super().update(request, *args, **kwargs)

        # Create operation log entry
        log_entry = OperationLog.objects.create(
            user=request.user,
            action=Action.UPDATE.value,
            model='WorkOrder',
            object_id=response.data['id'],
            details=f"Updated by {request.user.username}"
        )

        return response

    def destroy(self, request, *args, **kwargs):
        # Get object before deletion
        instance = self.get_object()

        # Perform delete action
        response = super().destroy(request, *args, **kwargs)

        # Create operation log entry
        log_entry = OperationLog.objects.create(
            user=request.user,
            action=Action.DELETE.value,
            model='WorkOrder',
            object_id=instance.id,
            details=f"Deleted by {request.user.username}"
        )

        return response
