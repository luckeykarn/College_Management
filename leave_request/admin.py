from django.contrib import admin
from .models import LeaveType,LeaveRequest


# Register your models here.
admin.site.register(LeaveType)
admin.site.register(LeaveRequest)


