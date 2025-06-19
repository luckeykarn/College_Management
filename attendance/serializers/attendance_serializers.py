from rest_framework import serializers
from ..models import Attendance
from employee.serializers.employee_serializers import EmployeeListSerializers
from employee.models import Employee
from datetime import datetime,time
from django.utils.timezone import localtime, now
# from attendance.serializers.attendance_serializers import AttendanceListSerializersAuthorize
class AttendanceListSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Attendance
        fields = ['id','status','check_in','check_out','worked_hours']

    
    def to_representation(self, instance):
        attrs =  super().to_representation(instance)
        user_obj = instance.employee.user
        department = instance.department
        attrs['full_name'] = f"{user_obj.first_name}  {user_obj.last_name}"
        attrs['department_name'] = department.name
        return attrs
        

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
        read_only_fields = ['worked_hours', 'remarks']

    #for single validation
    def validate_employee(self, value):
        # Check if department with this name already exists (case-insensitive)
        if Employee.objects.filter(employee=value).exists():
            return value
        else:
            raise serializers.ValidationError("Employee not exists.")
        
#    from datetime import datetime, time, timedelta
# Multiple validation of attributes
def validate(self, attrs):
    attrs = super().validate(attrs)

    status = attrs.get('status')
    check_in = attrs.get('check_in')
    check_out = attrs.get('check_out')

    # Standard office times
    standard_start = time(9, 0)   # 9:00 AM
    standard_end = time(17, 0)    # 5:00 PM

    # Attendance date
    attendance_date = (
        attrs.get('date') or
        getattr(self.instance, 'date', None) or
        datetime.today().date()
    )

    # Default remarks
    remarks = None

    if status == "Absent":
        attrs['check_in'] = None
        attrs['check_out'] = None
        attrs['worked_hours'] = None
        remarks = "Absent"

    elif status == "Leave":
        attrs['check_in'] = None
        attrs['check_out'] = None
        attrs['worked_hours'] = None
        remarks = "N/A"

    else:
        if not check_in or not check_out:
            raise serializers.ValidationError("Check-in and Check-out are required for Present or Half-Day.")

        start = datetime.combine(attendance_date, check_in)
        end = datetime.combine(attendance_date, check_out)

        if end <= start:
            raise serializers.ValidationError("Check-out time must be after Check-in time.")

        # Calculate worked hours
        delta = end - start
        worked_hours = round(delta.total_seconds() / 3600, 2)
        attrs['worked_hours'] = worked_hours

        # Auto remarks logic
        if worked_hours < 4:
            remarks = "Half-Day"
        elif check_in > standard_start:
            remarks = "Late"
        elif check_out < standard_end:
            remarks = "Early Leave"
        else:
            remarks = "On-Time"

    attrs['remarks'] = remarks
    return attrs
