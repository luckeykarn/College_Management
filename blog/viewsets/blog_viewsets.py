from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import status
# For caching import start
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache
# For caching import end


from ..models import Blog
from ..serializers.blog_serializers import (
    BlogListSerializers,
    BlogRetrieveSerializers,
    BlogWriteSerializers
)
from ..utilities.importbase import MyPageNumberPagination, blogPermission


class blogViewsets(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogListSerializers
    permission_classes = [IsAuthenticated,blogPermission]
    # pagination_class = MyPageNumberPagination

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id', 'title']
    ordering_fields = ['id', 'title']
    filterset_fields = {
        'id': ['exact'],
        'user': ['exact'],
        'tags': ['exact']
    }

    def get_queryset(self):
        current_user = self.request.user 
        # print(user," this is use called in get_queryset")
        # print(current_user.role)
        if current_user.role == "Admin":
            blogs = super().get_queryset()#Blog.objects.all()
            return blogs
        elif current_user.role == "Employee":
            blogs = super().get_queryset().filter(user = current_user)
            # print("this is employee login, and getting there blog,",blogs)
            return blogs
        else:
            # print(current_user.role)
            return super().get_queryset().none()

        

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return BlogWriteSerializers
        elif self.action == 'retrieve':
            return BlogRetrieveSerializers
        return super().get_serializer_class()
    
    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     serializer = self.get_serializer(queryset, many=True)

    #     return Response({
    #         "message": "Blogs fetched successfully.",
    #         "count": len(serializer.data),
    #         "data": serializer.data
    #     }, status=status.HTTP_200_OK)

    # Implementing Cache
    def list(self, request, *args, **kwargs):
        cache_key = "bloglist_cache_key"
        timeout = 300  # 5 minutes

        # Try to fetch from cache
        cached_response = cache.get(cache_key)
        if cached_response:
            print("Cache HIT - using cached data, Second_HIT")
            return Response(cached_response, status=status.HTTP_200_OK)

        # Generate fresh data (CACHE MISS)
        print("Cache MISS - generating fresh data, First_HIT")
        queryset = self.filter_queryset(self.get_queryset().order_by('id', 'title', 'tags'))
        serializer = self.get_serializer(queryset, many=True)

        # Store the response in a variable
        response_data = {
            "message": "Blogs fetched successfully.",
            "count": len(serializer.data),
            "data": serializer.data
        }

        # Cache it
        cache.set(cache_key, response_data, timeout=timeout)

        # Return the response
        return Response(response_data, status=status.HTTP_200_OK)

    
    def create(self, request, *args, **kwargs):
        title = request.data.get('title')
        tags = request.data.get('tags')  # assuming CharField
        user = request.user

        if Blog.objects.filter(title=title, tags=tags, user=user).exists():
            return Response({
                "message": "A blog with the same title and tags already exists.",
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)

        response = super().create(request, *args, **kwargs)
        return Response({
            "message": "Blog created successfully.",
            "data": response.data
        }, status=status.HTTP_201_CREATED)
    

    # def list(self, request, *args, **kwargs):
    #     """List blogs with caching - cache DATA, not Response object"""
    #     cache_key = f'blog_list_user_{request.user.id}'
        
    #     # Try to get cached DATA (not Response object)
    #     cached_data = cache.get(cache_key)
        
    #     if cached_data is not None:
    #         print("Returning from CACHE")
    #         # Return new Response with cached data
    #         return Response(cached_data)
        
    #     print("Returning from DATABASE")
    #     # Get fresh data from database
    #     response = super().list(request, *args, **kwargs)
        
    #     # Cache the DATA from the response, not the response object itself
    #     cache.set(cache_key, response.data, timeout=60)
        
    #     return response

