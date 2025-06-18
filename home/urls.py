from . import views
from django.urls import path

urlpatterns = [
path('', views.home,name="home"),
path('create-employee/', views.create_employee,name="create_employee"),
# path('api/create-employee/', views.CreateEmployeeAPIView.as_view(), name='create-employee'),

]