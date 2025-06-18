from django.shortcuts import render
from django.http import HttpResponse
from faker import Faker
import random
from datetime import date
from employee.models import Employee
from .models import Salary

# Create your views here.


def generate_fake_salaries(request):
    fake = Faker()
    employees = Employee.objects.all()

    if not employees:
        return HttpResponse("No employees found to generate salary data.", status=400)

    statuses = ['Paid', 'Pending', 'On Hold']
    payment_methods = ['Bank Transfer', 'Cash', 'Cheque']

    for employee in employees:
        for _ in range(2):  # Generate 2 salary records per employee
            month = random.randint(1, 12)
            year = random.choice([2023, 2024, 2025])

            basic_salary = random.randint(20000, 50000)
            bonus = random.randint(1000, 5000)
            deductions = random.randint(500, 3000)

            status = random.choice(statuses)
            payment_method = random.choice(payment_methods)

            paid_on = fake.date_between(start_date='-30d', end_date='today') if status == 'Paid' else None

            Salary.objects.create(
                employee=employee,
                month=month,
                year=year,
                basic_salary=basic_salary,
                bonus=bonus,
                deductions=deductions,
                net_salary=(basic_salary + bonus - deductions),
                amount=(basic_salary + bonus - deductions),  # Syncing for now
                paid_on=paid_on,
                status=status,
                payment_method=payment_method,
                remarks=fake.sentence()
            )

    return HttpResponse("Fake salary records generated successfully!")
