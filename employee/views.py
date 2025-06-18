from django.shortcuts import render
from .models import Department
from .models import CustomUser
from .models import Employee
import random
from faker import Faker
from django.http import HttpResponse

def random_employee_create(request):
    fake = Faker()
    user_ids = list(CustomUser.objects.values_list('id', flat=True))
    department_ids = list(Department.objects.values_list('id', flat=True))

    if not user_ids or not department_ids:
        return HttpResponse("No users or departments available.", status=400)

    for _ in range(50):  # Create 50 employees
        user_id = random.choice(user_ids)
        department_id = random.choice(department_ids)
        salary = round(random.uniform(20000, 80000), 2)
        hire_date = fake.date_this_decade()

        # Prevent duplicate employee entries for same user
        if not Employee.objects.filter(user_id=user_id).exists():
            Employee.objects.create(
                user_id=user_id,
                department_id=department_id,
                current_salary=salary,
                hire_date=hire_date
            )

    return HttpResponse("Random employees created!")


