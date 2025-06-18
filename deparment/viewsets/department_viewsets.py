from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Department
from employee.models import Employee
from ..serializers.department_serializers import DepartmentListSerializers, DepartmentListSerializersAuthorized, DepartmentRetrieveSerializers, DepartmentWriteSerializers
from ..utilities.importbase import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
# For caching import start
# from django.views.decorators.cache import cache_page
# from django.utils.decorators import method_decorator
from django.core.cache import cache
# For caching import end



class departmentViewsets(viewsets.ModelViewSet):
    serializer_class = DepartmentListSerializers
    permission_classes = [IsAuthenticated,deparmentPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = Department.objects.all()

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']

    filterset_fields = {
        'id': ['exact'],
        'name': ['exact'],
    }


    def get_queryset(self):
        user = self.request.user
        print(user)
        print(user.id)
        if user.role in ["Admin","Hr"]:
            deparments = super().get_queryset()  # Department.objects.all()
            return deparments
        

        elif user.role == "Employee":
            department = user.employee_profile.department
            return Department.objects.filter(id=department.id)

        else:
            return super().get_queryset().none()


    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return DepartmentWriteSerializers
        elif self.action == 'retrieve':
            
            return DepartmentRetrieveSerializers
        else:
            if self.request.user.role == "Admin" or self.request.user.role == "Hr":
                return DepartmentListSerializersAuthorized
            else:
                return DepartmentListSerializers

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        data = serializer.data  # serialized data after saving
        return Response({
            "message": "Department created successfully.",
            "data": data
        }, status=status.HTTP_201_CREATED)
    
    # @method_decorator(cache_page(60 * 5), name='list')  # 5 minutes cache
    # def list(self, request, *args, **kwargs):
    #     print("without cache *******")
    #    # Get queryset with explicit ordering
    #     queryset = self.filter_queryset(self.get_queryset().order_by('id'))  # order by 'id' or any field
        
    #     page = self.paginate_queryset(queryset)
    #     serializer = self.get_serializer(page, many=True) if page else self.get_serializer(queryset, many=True)

    #     response_data = {
    #         "message": "Department list fetched successfully.",
    #         "data": serializer.data
    #     }

    #     if page is not None:
    #         return self.get_paginated_response(response_data)

    #     return Response(response_data, status=status.HTTP_200_OK)


    def list(self, request, *args, **kwargs):
        cache_key = "my_department_list_cache_key"
        cached_response = cache.get(cache_key)

        if cached_response:
            print("Cache HIT")
            return Response(cached_response, status=status.HTTP_200_OK)
        
        print("Cache MISS")
        queryset = self.filter_queryset(self.get_queryset().order_by('id'))
        serializer = self.get_serializer(queryset, many=True)

        response_data = {
            "message": "Department list fetched successfully.",
            "count": len(serializer.data),
            "data": serializer.data
        }

        # Cache the response for 5 minutes (300 seconds)
        cache.set(cache_key, response_data, timeout=300)

        return Response(response_data, status=status.HTTP_200_OK)