from rest_framework import serializers
from ..models import LeaveType

class LeaveTypeListSerializers(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = '__all__'

class LeaveTypeRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = '__all__'

class LeaveTypeWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = '__all__'