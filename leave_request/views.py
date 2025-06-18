from django.shortcuts import render
from django.http import HttpResponse
from .models import LeaveRequest
from employee.models import Employee
from faker import Faker
import random
from datetime import timedelta

# Create your views here.


def fake_leave_requests(request):
    fake = Faker()
    employees = Employee.objects.all()

    if not employees.exists():
        return HttpResponse("No employee data found!", status=400)

    for _ in range(100):
        employee = random.choice(employees)
        
        start_date = fake.date_between(start_date='-30d', end_date='today')
        leave_duration = random.randint(1, 5)
        end_date = start_date + timedelta(days=leave_duration)

        reason = fake.sentence(nb_words=8)
        status = random.choice(['Pending', 'Approved', 'Rejected'])

        LeaveRequest.objects.create(
            employee=employee,
            start_date=start_date,
            end_date=end_date,
            reason=reason,
            status=status
        )

    return HttpResponse("100 fake leave requests created successfully!")
