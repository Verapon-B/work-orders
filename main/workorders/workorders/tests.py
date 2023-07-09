from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import WorkOrder, Cleaning
from django.contrib.auth import get_user_model
from .choices import WorkOrderType, WorkOrderStatus, UserRole

User = get_user_model()

class WorkOrderViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.work_order_url = reverse('workorder-list')
        self.user_supervisor = User.objects.create_user(username='supervisor1', password='password', role=UserRole.SUPERVISOR)
        self.user_guest = User.objects.create_user(username='guest1', password='password', role=UserRole.GUEST)
        self.create_work_order_data = {
            "work_order_number": "WO001",
            "room": "101",
            "started_at": "2023-07-08T10:00:00Z",
            "finished_at": "2023-07-08T12:00:00Z",
            "work_order_type": WorkOrderType.CLEANING.value,
            "status": WorkOrderStatus.ASSIGNED,
        }

    def test_create_work_order(self):
        self.client.force_authenticate(user=self.user_supervisor)
        self.create_work_order_data['created_by'] = self.user_supervisor.id
        self.create_work_order_data['assigned_to'] = self.user_guest.id
        response = self.client.post(self.work_order_url, self.create_work_order_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WorkOrder.objects.count(), 1)
        self.assertEqual(WorkOrder.objects.first().work_order_number, "WO001")

    def test_create_invalid_work_order(self):
        self.client.force_authenticate(user=self.user_supervisor)
        self.create_work_order_data['created_by'] = self.user_supervisor.id
        self.create_work_order_data['assigned_to'] = self.user_guest.id
        self.create_work_order_data['work_order_type'] = "InvalidType"
        response = self.client.post(self.work_order_url, self.create_work_order_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(WorkOrder.objects.count(), 0)

    def test_retrieve_work_order(self):
        work_order = WorkOrder.objects.create(created_by=self.user_supervisor, assigned_to=self.user_guest, **self.create_work_order_data)
        self.client.force_authenticate(user=self.user_supervisor)
        retrieve_url = reverse('workorder-detail', args=[work_order.id])
        response = self.client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['work_order_number'], "WO001")

    def test_update_work_order(self):
        work_order = WorkOrder.objects.create(created_by=self.user_supervisor, assigned_to=self.user_guest, **self.create_work_order_data)
        self.client.force_authenticate(user=self.user_supervisor)
        update_url = reverse('workorder-detail', args=[work_order.id])
        update_data = {
            "work_order_number": "WO001",
            "created_by": self.user_supervisor.id,
            "assigned_to": self.user_guest.id,
            "room": "101",
            "started_at": "2023-07-08T10:00:00Z",
            "finished_at": "2023-07-08T12:00:00Z",
            "work_order_type": WorkOrderType.CLEANING,
            "status": WorkOrderStatus.DONE,
        }
        response = self.client.put(update_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], WorkOrderStatus.DONE)

    def test_delete_work_order(self):
        work_order = WorkOrder.objects.create(created_by=self.user_supervisor, assigned_to=self.user_guest, **self.create_work_order_data)
        self.client.force_authenticate(user=self.user_supervisor)
        delete_url = reverse('workorder-detail', args=[work_order.id])
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(WorkOrder.objects.count(), 0)

    def test_update_cleaning_work_order_by_supervisor(self):
        work_order = WorkOrder.objects.create(
            created_by=self.user_supervisor,
            assigned_to=self.user_guest,
            **self.create_work_order_data
        )
        cleaning = Cleaning.objects.create(work_order=work_order)
        
        self.client.force_authenticate(user=self.user_supervisor)
        update_url = reverse('workorder-detail', args=[work_order.id])
        update_data = {
            "cancel_by_guest": True
        }
        response = self.client.patch(update_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cleaning.refresh_from_db()
        self.assertTrue(cleaning.cancel_by_guest)
