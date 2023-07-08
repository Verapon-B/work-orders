from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import WorkOrder
from .serializers import WorkOrderSerializer

class WorkOrderViewSet(viewsets.ModelViewSet):
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderSerializer

    def create(self, request, *args, **kwargs):
        work_order_type = request.data.get('type')
        user_role = None
        if request.user.is_authenticated:
            user_role = request.user.role

        if work_order_type == 'Cleaning':
            if user_role == 'supervisor':
                return super().create(request, *args, **kwargs)
            else:
                return Response({'error': 'Only Maid Supervisor can create Cleaning work orders.'}, status=status.HTTP_403_FORBIDDEN)

        if work_order_type == 'Maid Request':
            if user_role == 'supervisor':
                return super().create(request, *args, **kwargs)
            else:
                return Response({'error': 'Only Maid Supervisor can create Maid Request work orders.'}, status=status.HTTP_403_FORBIDDEN)

        if work_order_type == 'Technician Request':
            if user_role == 'guest' or user_role == 'supervisor':
                return super().create(request, *args, **kwargs)
            else:
                return Response({'error': 'Guests or Supervisors can create Technician Request work orders.'}, status=status.HTTP_403_FORBIDDEN)

        if work_order_type == 'Amenity Request':
            if user_role == 'guest':
                return super().create(request, *args, **kwargs)
            else:
                return Response({'error': 'Only guests can create Amenity Request work orders.'}, status=status.HTTP_403_FORBIDDEN)

        return Response({'error': 'Invalid work order type.'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user_role = None
        if request.user.is_authenticated:
            user_role = request.user.role

        if instance.type == 'Cleaning':
            if user_role == 'supervisor':
                return super().update(request, *args, **kwargs)
            else:
                return Response({'error': 'Only Maid Supervisor can update Cleaning work orders.'}, status=status.HTTP_403_FORBIDDEN)

        return super().update(request, *args, **kwargs)
