from rest_framework.routers import DefaultRouter
from ..viewsets.attendance_viewsets import attendanceViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('attendance', attendanceViewsets, basename="attendanceViewsets")
