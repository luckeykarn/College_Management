from django.urls import path
from . import views

urlpatterns = [
    path('generate-fake-salaries/', views.generate_fake_salaries),
]
