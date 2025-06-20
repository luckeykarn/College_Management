from django.db import models
from datetime import datetime
from django.utils.timezone import localtime, now
from deparment.models import Department
from employee.models import Employee

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Leave', 'Leave'),
        ('Half-Day', 'Half-Day'),
    ]

    REMARKS_CHOICES = [
        ('On-Time', 'On-Time'),
        ('Late', 'Late'),
        ('Early Leave', 'Early Leave'),
        ('Half-Day', 'Half-Day'),
        ('Absent', 'Absent'),
        ('N/A', 'N/A'),  # For Leave
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendances')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='attendances')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Present')
    date = models.DateField(auto_now_add=True)
    check_in = models.TimeField(blank=True, null=True)
    check_out = models.TimeField(blank=True, null=True)
    worked_hours = models.FloatField(blank=True, null=True)  # In decimal hours (e.g., 6.25)
    remarks = models.CharField(max_length=20, choices=REMARKS_CHOICES, blank=True, null=True)
    reason = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
    # Ensure `self.date` is set before calculating worked_hours
        if not self.date:
            self.date = datetime.today().date()

        # Only calculate if both check_in and check_out are provided
        if self.check_in and self.check_out:
            try:
                start = datetime.combine(self.date, self.check_in)
                end = datetime.combine(self.date, self.check_out)

                if end > start:
                    delta = end - start
                    self.worked_hours = round(delta.total_seconds() / 3600, 2)
                else:
                    self.worked_hours = None  # Avoid negative or zero durations
            except Exception as e:
                self.worked_hours = None  # Handle unexpected issues gracefully
        else:
            self.worked_hours = None

        super().save(*args, **kwargs)


    def formatted_check_in(self):
        return self.check_in.strftime('%I:%M %p') if self.check_in else "N/A"

    def formatted_check_out(self):
        return self.check_out.strftime('%I:%M %p') if self.check_out else "N/A"

    def __str__(self):
        return f"{self.employee} - {self.status} on {self.date}"
