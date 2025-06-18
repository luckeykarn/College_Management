from rest_framework.routers import DefaultRouter
from ..viewsets.salary_viewsets import salaryViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('salary', salaryViewsets, basename="salaryViewsets")
