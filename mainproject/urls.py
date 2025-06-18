"""
URL configuration for mainproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from debug_toolbar.toolbar import debug_toolbar_urls

#for implementation of swagger
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
# from rest_framework_simplejwt.authentication import JWTAuthentication

#*********This is blog router registered by autoapi*********
from rest_framework import routers
from blog.routers.routers import router as blog_router
from accounts.routers.routers import router as accounts_router
from deparment.routers.routers import router as deparment_router
from employee.routers.routers import router as employee_router
from attendance.routers.routers import router as attendance_router
from leave_request.routers.routers import router as leave_request_router
from salaries.routers.routers import router as salaries_router
# urlpatterns.append(path('api/',include(blog_router.urls)))
router = routers.DefaultRouter()
router.registry.extend(blog_router.registry)
router.registry.extend(accounts_router.registry)
router.registry.extend(deparment_router.registry)
router.registry.extend(employee_router.registry)
router.registry.extend(attendance_router.registry)
router.registry.extend(leave_request_router.registry)
router.registry.extend(salaries_router.registry)



schema_view = get_schema_view(
   openapi.Info(
      title="College HR System",
      default_version='v1',
      description="API Testing for College_HR_System",
      contact=openapi.Contact(email="luckeykarn11@gmail.com"),
   
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
#    authentication_classes=[JWTAuthentication],
    authentication_classes=[],
)

from accounts.login.login_views import CustomTokenRefreshView, CustomTokenObtainPairViewAdmin, CustomTokenObtainPairViewHr, CustomTokenObtainPairViewEmployee , CustomTokenRefreshView
from accounts.viewsets.customuser_viewsets import CreateUserAPIView
from employee.viewsets.employee_viewsets import CreateEmployeeAPIView

urlpatterns = [
    path('api/auth/refresh-token/', CustomTokenRefreshView.as_view(), name='CustomTokenRefreshView'),
    path('api/auth/admin/login/', CustomTokenObtainPairViewAdmin.as_view(), name='token_obtain_pair_admin'),
    path('api/auth/hr/login/', CustomTokenObtainPairViewHr.as_view(), name='CustomTokenObtainPairViewHr'),
    path('api/auth/employee/login/', CustomTokenObtainPairViewEmployee.as_view(), name='CustomTokenObtainPairViewEmployee'),
    # path('api/register/', RegisterView.as_view({'post': 'create'}), name='RegisterView'),
    path('api/auth/register/', CreateUserAPIView.as_view(), name='create-user'),
    path('api/create-employee/', CreateEmployeeAPIView.as_view(), name='create-employee'),

    path("api/",include(router.urls)),
   
    path('admin/', admin.site.urls),
    path('blog/',include("blog.urls")),
    path('attendance/',include("attendance.urls")),
    path('accounts/',include("accounts.urls")),
    path('employee/',include("employee.urls")),
    path('leave-request/',include("leave_request.urls")),
    path('salaries/',include("salaries.urls")),
    path('',include("home.urls")),

     # API Endpoints
    # path('api/auth/', include('accounts.accounts_api.api_urls')),
    # path('api/department/', include('deparment.department_api.api_urls')),
    # path('api/employee/', include('employee.employee_api.api_urls')),

    # Swagger and Redoc URLs
    path('swagger.<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]+ debug_toolbar_urls()


#*********This is attendance router registered by autoapi*********
from attendance.routers.routers import router as attendance_router
urlpatterns.append(path('api/',include(attendance_router.urls)))
#*********This is leave_request router registered by autoapi*********
from leave_request.routers.routers import router as leave_request_router
urlpatterns.append(path('api/',include(leave_request_router.urls)))
#*********This is salaries router registered by autoapi*********
from salaries.routers.routers import router as salaries_router
urlpatterns.append(path('api/',include(salaries_router.urls)))
#*********This is deparment router registered by autoapi*********
from deparment.routers.routers import router as deparment_router
urlpatterns.append(path('api/',include(deparment_router.urls)))
#*********This is employee router registered by autoapi*********
from employee.routers.routers import router as employee_router
urlpatterns.append(path('api/',include(employee_router.urls)))