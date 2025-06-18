from rest_framework.routers import DefaultRouter
from ..viewsets.leavetype_viewsets import leavetypeViewsets
from ..viewsets.leaverequest_viewsets import leaverequestViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('leavetype', leavetypeViewsets, basename="leavetypeViewsets")
router.register('leaverequest', leaverequestViewsets, basename="leaverequestViewsets")
