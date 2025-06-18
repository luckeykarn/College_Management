from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import TokenObtainPairView
from ..serializers.customuser_serializers import CustomTokenRefreshSerializer,CustomTokenObtainPairSerializerAdmin,CustomTokenObtainPairSerializerHr,CustomTokenObtainPairSerializerEmployee

from rest_framework_simplejwt.views import TokenRefreshView
# from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# from rest_framework import status


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer

    @swagger_auto_schema(
        operation_description="Refresh access token using a valid refresh token.",
        tags=['Auth'],
        request_body=CustomTokenRefreshSerializer,
        responses={200: openapi.Response('Access token refreshed')}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)



class CustomTokenObtainPairViewAdmin(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializerAdmin

    @swagger_auto_schema(
    operation_description="Admin login to get JWT token",
    tags=['Auth']
)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)



class CustomTokenObtainPairViewHr(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializerHr

    @swagger_auto_schema(
    operation_description="HR login to get JWT token",
    tags=['Auth']
)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomTokenObtainPairViewEmployee(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializerEmployee

    @swagger_auto_schema(
    operation_description="Employee login to get JWT token",
    tags=['Auth']
)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
        