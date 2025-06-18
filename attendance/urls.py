from django.urls import path
from . import views
urlpatterns = [
    path('random-attendance-create/', views.random_attendance),
    
]