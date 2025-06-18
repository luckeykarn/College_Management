from rest_framework import serializers
from ..models import Salary

class SalaryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Salary
        fields = '__all__'

class SalaryRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Salary
        fields = '__all__'

class SalaryWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Salary
        fields = '__all__'