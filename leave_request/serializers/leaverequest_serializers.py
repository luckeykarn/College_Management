from rest_framework import serializers
from ..models import LeaveRequest

class LeaveRequestListSerializers(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = '__all__'

class LeaveRequestRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = '__all__'

class LeaveRequestWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = '__all__'