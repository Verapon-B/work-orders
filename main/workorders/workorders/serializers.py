from rest_framework import serializers
from .models import WorkOrder, MaidRequest, TechnicianRequest, AmenityRequest

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

class WorkOrderSerializer(serializers.ModelSerializer):
    maid_request = MaidRequestSerializer(required=False)
    technician_request = TechnicianRequestSerializer(required=False)
    amenity_request = AmenityRequestSerializer(required=False)

    class Meta:
        model = WorkOrder
        fields = '__all__'

    def create(self, validated_data):
        maid_request_data = validated_data.pop('maid_request', None)
        technician_request_data = validated_data.pop('technician_request', None)
        amenity_request_data = validated_data.pop('amenity_request', None)

        work_order = WorkOrder.objects.create(**validated_data)

        if maid_request_data:
            MaidRequest.objects.create(work_order=work_order, **maid_request_data)
        if technician_request_data:
            TechnicianRequest.objects.create(work_order=work_order, **technician_request_data)
        if amenity_request_data:
            AmenityRequest.objects.create(work_order=work_order, **amenity_request_data)

        return work_order
