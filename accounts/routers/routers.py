from django.urls import path
from rest_framework.routers import DefaultRouter
from ..viewsets.customuser_viewsets import customuserViewsets
# from rest_framework_simplejwt.views import TokenRefreshView
# from accounts.viewsets.customuser_viewsets import RegisterView

# Initialize the router
router = DefaultRouter()
auto_api_routers = router

router.register('customuser', customuserViewsets, basename="customuserViewsets")

# router.register('register', RegisterView, basename='register')
