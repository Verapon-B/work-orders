from django.db import models
from django.utils.translation import gettext_lazy as _


class Action(models.TextChoices):
    CREATE = 'create', _('Create'),
    UPDATE = 'update', _('Update'),
    DELETE = 'delete', _('Delete'),

class WorkOrderType(models.TextChoices):
    CLEANING = 'cleaning', _('Cleaning')
    MAID_REQUEST = 'maid_request', _('Maid Request')
    TECHNICIAN_REQUEST = 'technician_request', _('Technician Request')
    AMENITY_REQUEST = 'amenity_request', _('Amenity Request')

class WorkOrderStatus(models.TextChoices):
    CREATED = 'created', _('Created')
    ASSIGNED = 'assigned', _('Assigned')
    IN_PROGRESS = 'in_progress', _('In Progress')
    DONE = 'done', _('Done')
    CANCEL = 'cancel', _('Cancel')

class UserRole(models.TextChoices):
    ADMIN = 'admin', _('Admin')
    SUPERVISOR = 'supervisor', _('Supervisor')
    GUEST = 'user', _('Guest')
    MAID = 'maid', _('Maid')

