from django.db import models
from django.contrib.auth.models import User

class WorkOrder(models.Model):
    WORK_ORDER_TYPES = (
        ('cleaning', 'Cleaning'),
        ('maid_request', 'Maid Request'),
        ('technician_request', 'Technician Request'),
        ('amenity_request', 'Amenity Request'),
    )

    WORK_ORDER_STATUSES = (
        ('created', 'Created'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
    )

    work_order_number = models.CharField(max_length=50, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_workorders')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_workorders')
    room = models.CharField(max_length=50)
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField()
    type = models.CharField(max_length=20, choices=WORK_ORDER_TYPES)
    status = models.CharField(max_length=20, choices=WORK_ORDER_STATUSES)

class MaidRequest(models.Model):
    work_order = models.OneToOneField(WorkOrder, on_delete=models.CASCADE, primary_key=True)
    description = models.TextField()

class TechnicianRequest(models.Model):
    work_order = models.OneToOneField(WorkOrder, on_delete=models.CASCADE, primary_key=True)
    defect_type = models.CharField(max_length=50)

class AmenityRequest(models.Model):
    work_order = models.OneToOneField(WorkOrder, on_delete=models.CASCADE, primary_key=True)
    amenity_type = models.CharField(max_length=50)
    quantity = models.IntegerField()
