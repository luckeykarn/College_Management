from rest_framework import serializers
from ..models import Attendance
from employee.serializers.employee_serializers import EmployeeListSerializers
# from attendance.serializers.attendance_serializers import AttendanceListSerializersAuthorize
class AttendanceListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id','status','check_in','check_out','worked_hours']

class AttendanceListSerializersAuthorize(serializers.ModelSerializer):
    employee = EmployeeListSerializers(read_only=True)
    class Meta:
        model = Attendance
        fields = ['id','status','check_in','check_out','worked_hours','employee']
    


class AttendanceRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

class AttendanceWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'