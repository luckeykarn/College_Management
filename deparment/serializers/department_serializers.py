from rest_framework import serializers
from ..models import Department
# from employee.models import Employee
from employee.serializers.employee_serializers import EmployeeListSerializers

class DepartmentListSerializers(serializers.ModelSerializer):
    # employees = EmployeeListSerializers(many=True, read_only=True)

    class Meta:
        model = Department
        fields = ['id','name']

class DepartmentListSerializersAuthorized(serializers.ModelSerializer):
    employees = EmployeeListSerializers(many=True, read_only=True)

    class Meta:
        model = Department
        fields = ['id','name','employees']


class DepartmentRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class DepartmentWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
    
    def validate_name(self, value):
        # Check if department with this name already exists (case-insensitive)
        if Department.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("Department with this name already exists.")
        return value