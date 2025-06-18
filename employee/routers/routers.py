from rest_framework.routers import DefaultRouter
from ..viewsets.employee_viewsets import employeeViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('employee', employeeViewsets, basename="employeeViewsets")
