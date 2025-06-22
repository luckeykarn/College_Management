from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import CustomUser
from ..serializers.customuser_serializers import UserCreateSerializerAdmin,CustomUserListSerializers, CustomUserRetrieveSerializers, CustomUserWriteSerializers,UserCreateSerializer
from ..utilities.importbase import *
from rest_framework_simplejwt.tokens import RefreshToken
# For caching import start
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache
# For caching import end
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
# For caching import start
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache
# For caching import end


from accounts.task import send_welcome_email
from django.http import JsonResponse

class customuserViewsets(viewsets.ModelViewSet):
    serializer_class = CustomUserListSerializers
    permission_classes = [accountsPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = CustomUser.objects.all()

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']

    filterset_fields = {
        'id': ['exact'],
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.role == 'Admin':
            users = super().get_queryset()#CustomUser.objects.all()
            return users
        else:
            # print(current_user.role)
            return super().get_queryset().none()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            if self.request.user.role == "Admin":
                # print("ehjgdhjegdhejgjheg")
                return UserCreateSerializerAdmin
            else:
                return UserCreateSerializer
        elif self.action == 'retrieve':
            return CustomUserRetrieveSerializers
        return CustomUserListSerializers
    
    
    # def list(self, request, *args, **kwargs):#without caching
    #     queryset = self.filter_queryset(self.get_queryset())
    #     serializer = self.get_serializer(queryset, many=True)

    #     return Response({
    #         "message": "Users fetched successfully.",
    #         "count": len(serializer.data),
    #         "data": serializer.data
    #     }, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        # Set cache key and timeout
        cache_key = "userlist_cache_key"
        timeout = 300  # 5 minutes (in seconds)

        # Get the cached response
        cached_response = cache.get(cache_key)

        # Step 3: If cache exists, return cached data (CACHE HIT)
        if cached_response:
            print("Cache HIT - using cached data,Second_HIT")
            return Response(cached_response, status=status.HTTP_200_OK)

        # If not found, generate data (CACHE MISS)
        print("Cache MISS - generating fresh data,First_HIT")
        queryset = self.filter_queryset(self.get_queryset().order_by('id','first_name','gender'))
        serializer = self.get_serializer(queryset, many=True)

        # Store the response in a variable
        response_data={
                "message": "Users fetched successfully.",
                "count": len(serializer.data),
                "data": serializer.data
            }

        # Set the new response into cache
        cache.set(cache_key, response_data, timeout=timeout)

        # Return the fresh data/reponse
        return Response(response_data, status=status.HTTP_200_OK)
    

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        data = serializer.data  # serialized data after saving

        return Response({
            "message": "User created successfully.",
            "data": data
        }, status=status.HTTP_201_CREATED)
    

class CreateUserAPIView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]  # You can restrict this if needed

    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)


        return Response({
            "message": "User created successfullys.",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)



    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import AllowAny
# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi


# class RegisterView(viewsets.ModelViewSet):
#     serializer_class = RegisterSerializer
#     permission_classes = [AllowAny]
#     queryset = CustomUser.objects.all()

#     @swagger_auto_schema(
#         operation_description="Register a new user. Only Admin can assign role & department.",
#         request_body=RegisterSerializer,
#         responses={
#             201: openapi.Response(
#                 description="User registered successfully",
#                 examples={
#                     "application/json": {
#                         "message": "Registration successful",
#                         "user": {
#                             "id": 1,
#                             "username": "newuser",
#                             "email": "newuser@example.com"
#                         },
#                         "tokens": {
#                             "refresh": "token123",
#                             "access": "token456"
#                         }
#                     }
#                 }
#             ),
#             400: "Bad Request"
#         }
#     )
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()

#         return Response({
#             'message': 'Registration successful',
#             'user': serializer.data,  # includes tokens
#         }, status=status.HTTP_201_CREATED)
    
#         # CACHE applied to LIST view
#     @method_decorator(cache_page(60 * 5))  # 5 minutes
#     def list(self, request, *args, **kwargs):
#         return super().list(request, *args, **kwargs)

