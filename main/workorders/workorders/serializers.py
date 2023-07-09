from rest_framework import serializers
from .models import WorkOrder, MaidRequest, TechnicianRequest, AmenityRequest, Cleaning

class MaidRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaidRequest
        fields = '__all__'

class TechnicianRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicianRequest
        fields = '__all__'

class AmenityRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmenityRequest
        fields = '__all__'

class CleaningSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cleaning
        fields = '__all__'

class WorkOrderSerializer(serializers.ModelSerializer):
    maid_request = MaidRequestSerializer(required=False)
    technician_request = TechnicianRequestSerializer(required=False)
    amenity_request = AmenityRequestSerializer(required=False)
    cleaning_request = CleaningSerializer(required=False)

    class Meta:
        model = WorkOrder
        fields = '__all__'
