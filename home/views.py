from django.shortcuts import render
from accounts.models import CustomUser
from employee.models import Employee
from deparment.models import Department
from rest_framework.response import Response
from django.http.response import HttpResponse

# Create your views here.
def home(request):
    context = {
        "title":"Homepage"
    }
    return render(request, "home.html",context)

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def create_employee(request):
    print("abcdef",request.method)
    if request.method == "POST":
        first_name = request.POST["first_name"]
        second_name = request.POST["second_name"]
        email = request.POST["email"]
        password = request.POST["password"]
        gender = request.POST["gender"]
        department = request.POST["department"]
        current_salary = request.POST["salary"]
        hire_date = request.POST["hire_date"]
        print(request.POST)

        create_user = CustomUser.objects.create(username=email,first_name = first_name,last_name = second_name,email = email,gender = gender,password = password)
        print(create_user)
        create_employee = Employee.objects.create(user = create_user,department_id = department,current_salary = current_salary,hire_date =  hire_date)
        return HttpResponse("Employee created successfully")

    else:
        print("abcdef",request.method)
        return HttpResponse("You don't have permission to perform this action")










