from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('random-blog-create/', views.random_blog),
    
]