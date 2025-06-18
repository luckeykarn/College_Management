from django.urls import path
from . import views
urlpatterns = [
    path('random-user-create/', views.random_user),
    path('login/', views.login,name="login"),
    path('signup/', views.signup,name="signup"),
    
    
]