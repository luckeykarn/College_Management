from django.db import models
from accounts.models import CustomUser
from deparment.models import Department


class Employee(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="employee_profile")
    department = models.ForeignKey(Department,related_name='employees', null=True, on_delete=models.SET_NULL)
    current_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    hire_date = models.DateField(null=True, blank=True)
    welcome_email_sent = models.BooleanField(default=False)


    created_at = models.DateTimeField(auto_now_add=True)  # set only on create
    updated_at = models.DateTimeField(auto_now=True)      # set on each update
   
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
