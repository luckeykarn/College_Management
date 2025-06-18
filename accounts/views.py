from django.shortcuts import render
from django.http import HttpResponse
from .models import CustomUser  # your extended user model
from faker import Faker
import random

from django.http import HttpResponse
from .models import CustomUser
from faker import Faker
import random

def random_user(request):
    fake = Faker('en_IN')  # English names common in India
    gender_list = ['Male', 'Female', 'Other']

    for _ in range(100):
        selected_gender = random.choice(gender_list)

        if selected_gender == 'Male':
            first_name = fake.first_name_male()
        elif selected_gender == 'Female':
            first_name = fake.first_name_female()
        else:
            # Random pick for 'Other'
            first_name = random.choice([fake.first_name_male(), fake.first_name_female()])

        last_name = fake.last_name()

        username = f"{first_name.lower()}{last_name.lower()}{random.randint(100, 999)}"
        email = f"{username}@example.com"

        user = CustomUser(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            gender=selected_gender  # use the correct gender here
        )
        user.set_password("password123")  #  hashes the password properly
        user.save()

    return HttpResponse(" 100 realistic fake users created successfully!")


def login(request):
    return render(request, "login.html")

def signup(request):
    return render(request, "signup.html")