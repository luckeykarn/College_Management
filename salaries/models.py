from django.db import models
from employee.models import Employee

class Salary(models.Model):
    PAYMENT_STATUS = [
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
        ('On Hold', 'On Hold'),
    ]
    
    PAYMENT_METHODS = [
        ('Bank Transfer', 'Bank Transfer'),
        ('Cash', 'Cash'),
        ('Cheque', 'Cheque'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.IntegerField()  # 1 to 12
    year = models.IntegerField()

    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Optional if net_salary used

    paid_on = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='Pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='Bank Transfer')
    remarks = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Auto-calculate net salary before saving
        self.net_salary = (self.basic_salary + self.bonus) - self.deductions
        self.amount = self.net_salary  # Optional sync
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.user.username} - {self.month}/{self.year} - {self.status}"
