from django.db import models
from employee.models import Employee

# Create your models here.
class LeaveType(models.Model):
    leavetype = models.CharField(max_length=50)  # Vacation, Sick, Personal
    days_allowed = models.PositiveIntegerField()

    def __str__(self):
        return self.leavetype


class LeaveRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(LeaveType, on_delete=models.SET_NULL, null=True) 
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.employee.user.username} - {self.leave_type} ({self.status})"
