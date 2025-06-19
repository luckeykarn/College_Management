from rest_framework import serializers
from ..models import Employee
from accounts.serializers.customuser_serializers import XotusaCustomUserListSerializers
from accounts.models import CustomUser


class EmployeeListSerializers(serializers.ModelSerializer):
    user = XotusaCustomUserListSerializers(read_only=True)
    class Meta:
        model = Employee
        fields =  ['id','user','current_salary','hire_date']


class EmployeeRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class EmployeeWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class EmployeeCreateSerializer(serializers.Serializer):
    # User fields
    first_name = serializers.CharField()
    second_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    gender = serializers.CharField()
    role = serializers.CharField()

    # Employee fields
    department = serializers.IntegerField()
    salary = serializers.DecimalField(max_digits=10, decimal_places=2)
    hire_date = serializers.DateField()

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        # Extract user fields
        user = CustomUser.objects.create(
            username=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["second_name"],
            email=validated_data["email"],
            gender=validated_data["gender"],
        )
        user.set_password(validated_data["password"])
        user.save()

        # Create employee record
        employee = Employee.objects.create(
            user=user,
            department_id=validated_data["department"],
            current_salary=validated_data["salary"],
            hire_date=validated_data["hire_date"],
        )

        # Return both in a dict
        return {
            "user": user,
            "employee": employee
        }

    def to_representation(self, instance):
        user = instance["user"]
        employee = instance["employee"]

        return {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "second_name": user.last_name,
            "gender": user.gender,
            "role": user.role,
            "department": employee.department.id,
            "salary": employee.current_salary,
            "hire_date": employee.hire_date,
        }



















    # first_name = serializers.CharField()
    # second_name = serializers.CharField()
    # email = serializers.EmailField()
    # password = serializers.CharField(write_only=True)
    # gender = serializers.CharField()
    # department = serializers.IntegerField()
    # salary = serializers.DecimalField(max_digits=10, decimal_places=2)
    # hire_date = serializers.DateField()

    # def create(self, validated_data):
    #     user = CustomUser.objects.create(
    #         username=validated_data["email"],
    #         first_name=validated_data["first_name"],
    #         last_name=validated_data["second_name"],
    #         email=validated_data["email"],
    #         gender=validated_data["gender"],
    #     )
    #     user.set_password(validated_data["password"])  # important: hash password!
    #     user.save()

    #     employee = Employee.objects.create(
    #         user=user,
    #         department_id=validated_data["department"],
    #         current_salary=validated_data["salary"],
    #         hire_date=validated_data["hire_date"],
    #     )
    #     return employee

    
