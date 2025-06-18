from django.shortcuts import render
from django.http import HttpResponse
from .models import Attendance
from employee.models import Employee
from deparment.models import Department
from datetime import time, datetime, timedelta
import random
from faker import Faker

def random_attendance(request):
    fake = Faker()
    employees = Employee.objects.select_related('user', 'department').all()

    if not employees.exists():
        return HttpResponse("No employees available to generate attendance.", status=400)

    for _ in range(100):
        employee = random.choice(employees)

        if not employee.department:
            continue

        status = random.choice(['Present', 'Absent', 'Leave', 'Half-Day'])
        date = fake.date_between(start_date='-30d', end_date='today')
        check_in = None
        check_out = None
        remarks = ""
        reason = ""
        worked_hours = None

        if status in ['Present', 'Half-Day']:
            check_in_hour = random.randint(8, 10)
            check_in_minute = random.randint(0, 59)
            check_in = time(hour=check_in_hour, minute=check_in_minute)

            check_out_hour = random.randint(16, 18)
            check_out_minute = random.randint(0, 59)
            check_out = time(hour=check_out_hour, minute=check_out_minute)

            # Calculate worked_hours as timedelta
            start = datetime.combine(date, check_in)
            end = datetime.combine(date, check_out)
            worked_hours = end - start

            if check_in_hour > 9 or (check_in_hour == 9 and check_in_minute > 0):
                remarks = "Late"
                reason = random.choice(["Traffic jam", "Overslept", "Bus delayed", "Power cut"])
            else:
                remarks = "On-time"

        elif status == "Absent":
            remarks = "Absent"
            reason = random.choice(["Sick", "No call/no show", "Family emergency"])

        elif status == "Leave":
            remarks = "Leave"
            reason = random.choice(["Medical leave", "Vacation", "Festival"])

        # ✅ Skip if duplicate attendance exists
        existing = Attendance.objects.filter(employee=employee, date=date).exists()
        if existing:
            continue

        # Save record
        Attendance.objects.create(
            employee=employee,
            department=employee.department,
            status=status,
            date=date,
            check_in=check_in,
            check_out=check_out,
            worked_hours=worked_hours,
            remarks=remarks,
            reason=reason
        )

    return HttpResponse("100 fake attendance records created successfully!")
