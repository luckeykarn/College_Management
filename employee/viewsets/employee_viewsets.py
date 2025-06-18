from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Employee
from ..serializers.employee_serializers import EmployeeListSerializers, EmployeeRetrieveSerializers, EmployeeWriteSerializers
from ..utilities.importbase import *
# For APIview
from rest_framework.generics import CreateAPIView
from accounts.models import CustomUser
from employee.serializers.employee_serializers import EmployeeCreateSerializer
from rest_framework.permissions import IsAuthenticated
from ..viewsets.permission import IsAdminOrHR
from rest_framework.response import Response
from rest_framework import status
# For redis caching import start
from django.core.cache import cache
# For caching import end

class employeeViewsets(viewsets.ModelViewSet):
    serializer_class = EmployeeListSerializers
    permission_classes = [employeePermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = Employee.objects.all()

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']

    filterset_fields = {
        'id': ['exact'],
        'hire_date': ['exact'],
        'department__name': ['exact', 'icontains'],  # filter by related department's name

        
    }

    def get_queryset(self):
        user = self.request.user

        if user.role == "Admin":
            return Employee.objects.all()

        elif user.role == "Hr":
            return  Employee.objects.all()

        elif user.role == "Employee":
            return Employee.objects.filter(user=user)

        return Employee.objects.none()

        
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return EmployeeWriteSerializers
        elif self.action == 'retrieve':
            return EmployeeRetrieveSerializers
        return super().get_serializer_class()
    
    # @method_decorator(cache_page(60 * 5))  # 5 minutes cache
    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response({
    #         "message": "Employee list fetched successfully.",
    #         "data": serializer.data
    #     }, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        cache_key = "employee_list_cache"
        timeout = 300  # 5 minutes

        # Try to get data from cache
        cached_response = cache.get(cache_key)
        if cached_response:
            print("Cache HIT")
            return Response(cached_response, status=status.HTTP_200_OK)

        # If not cached, fetch from DB
        print("Cache MISS")
        queryset = self.filter_queryset(self.get_queryset().order_by('id'))
        serializer = self.get_serializer(queryset, many=True)

        # Create pure dictionary for caching
        response_data = {
            "message": "Employee list fetched successfully.",
            "count": len(serializer.data),
            "data": serializer.data
        }

        # Cache raw dictionary, not Response object
        cache.set(cache_key, response_data, timeout=timeout)

        # Return DRF Response with dictionary
        return Response(response_data, status=status.HTTP_200_OK)


    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)


class CreateEmployeeAPIView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = EmployeeCreateSerializer
    permission_classes = [IsAuthenticated,IsAdminOrHR]  # You can restrict this if needed


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created_data = serializer.save()

        return Response({
            "message": "Employee created successfully.",
            "data": serializer.to_representation(created_data)
        }, status=status.HTTP_201_CREATED)
    
   
    