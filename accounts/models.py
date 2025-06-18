from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('HR', 'HR'),
        ('Employee', 'Employee'),
        ('User', 'User'),
        # ('Students', 'Students'),
        # ('Staff', 'Staff'),

    )
    # myblogs = 
    role = models.CharField(max_length=10, choices=ROLE_CHOICES,default="User")

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('others', 'Others'),
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    # @property
    # def name(self):
    #         return f"{self.first_name} {self.last_name}"

# def __str__(self):
#         return self.name
