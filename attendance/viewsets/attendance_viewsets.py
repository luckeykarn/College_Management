from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Attendance
from ..serializers.attendance_serializers import AttendanceListSerializersAuthorize,AttendanceListSerializers, AttendanceRetrieveSerializers, AttendanceWriteSerializers
from ..utilities.importbase import *
from rest_framework.permissions import IsAuthenticated

class attendanceViewsets(viewsets.ModelViewSet):
    serializer_class = AttendanceListSerializers
    permission_classes = [IsAuthenticated,attendancePermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = Attendance.objects.all()

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']

    # filterset_fields = {
    #     'id': ['exact'],
    # }

    def get_queryset(self):
       user = self.request.user
       if user.role in ["Admin","Hr"]:
           attendance = super().get_queryset()
           return attendance
       elif user.role == "Employee":
            return Attendance.objects.filter(id=attendance.id)
       else:
            return super().get_queryset().none()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return AttendanceWriteSerializers
        elif self.action == 'retrieve':
            return AttendanceRetrieveSerializers
        else:
            if self.request.user.role == "Admin" or self.request.user.role == "Hr":
                print("this is list action for hr and admin")
                return AttendanceListSerializersAuthorize
            else:
                print("this is list action for hr and admin",self.request.user.role)
                return AttendanceListSerializers

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)