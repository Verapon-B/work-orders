from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import WorkOrder
from .serializers import WorkOrderSerializer

class WorkOrderViewSet(viewsets.ModelViewSet):
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderSerializer

    def create(self, request, *args, **kwargs):
        # Get the work order type from the request data
        work_order_type = request.data.get('type')

        # Check the work order type and apply specific rules
        if work_order_type == 'Cleaning':
            # Check if the user creating the work order is the Maid Supervisor
            if request.user.is_authenticated and request.user.is_superuser:
                return super().create(request, *args, **kwargs)
            else:
                return Response({'error': 'Only Maid Supervisor can create Cleaning work orders.'}, status=status.HTTP_403_FORBIDDEN)

        if work_order_type == 'Maid Request':
            # Check if the user creating the work order is the Maid Supervisor
            if request.user.is_authenticated and request.user.is_superuser:
                return super().create(request, *args, **kwargs)
            else:
                return Response({'error': 'Only Maid Supervisor can create Maid Request work orders.'}, status=status.HTTP_403_FORBIDDEN)

        if work_order_type == 'Technician Request':
            # Allow both guests and supervisors to create Technician Request work orders
            return super().create(request, *args, **kwargs)

        if work_order_type == 'Amenity Request':
            # Check if the user creating the work order is a guest
            if request.user.is_authenticated and not request.user.is_superuser:
                return super().create(request, *args, **kwargs)
            else:
                return Response({'error': 'Only guests can create Amenity Request work orders.'}, status=status.HTTP_403_FORBIDDEN)

        return Response({'error': 'Invalid work order type.'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # Check if the work order type is 'Cleaning'
        if instance.type == 'Cleaning':
            # Check if the user updating the work order is the Maid Supervisor
            if request.user.is_authenticated and request.user.is_superuser:
                return super().update(request, *args, **kwargs)
            else:
                return Response({'error': 'Only Maid Supervisor can update Cleaning work orders.'}, status=status.HTTP_403_FORBIDDEN)

        # For other work order types, allow the update
        return super().update(request, *args, **kwargs)
