from rest_framework.routers import DefaultRouter
from ..viewsets.blog_viewsets import blogViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('blog', blogViewsets, basename="blogViewsets")
