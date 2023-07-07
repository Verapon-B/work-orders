from django.contrib import admin
from django.urls import path
from workorders.views import WorkOrder

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/workorders/', WorkOrder),
]
