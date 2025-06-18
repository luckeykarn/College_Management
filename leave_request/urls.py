from django.urls import path
from . import views

urlpatterns = [
    path('generate-fake-leaves/', views.fake_leave_requests, name='generate_fake_leaves'),
]
