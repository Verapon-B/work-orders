from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from .choices import Action, UserRole, WorkOrderType, WorkOrderStatus

class User(AbstractUser):
    role = models.CharField(max_length=20, choices=UserRole.choices)

class WorkOrder(models.Model):
    work_order_number = models.CharField(max_length=50, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_workorders')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_workorders')
    room = models.CharField(max_length=50)
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField()
    work_order_type = models.CharField(max_length=20, choices=WorkOrderType.choices)
    status = models.CharField(max_length=20, choices=WorkOrderStatus.choices)

class Cleaning(models.Model):
    work_order = models.OneToOneField(WorkOrder, on_delete=models.CASCADE, primary_key=True)
    cancel_by_guest = models.BooleanField(default=False)

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

class OperationLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    action = models.CharField(max_length=10, choices=Action.choices)
    model = models.CharField(max_length=100)
    object_id = models.PositiveIntegerField()
    details = models.TextField()

    def __str__(self):
        return f"{self.action} on {self.model} ({self.object_id})"
