from django.urls import path

from .apps import UsersConfig
from users import views

app_name = UsersConfig.name

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('register/', views.UserCreateView.as_view(), name='register'),
    path('profile/<int:pk>/', views.UserUpdateView.as_view(), name='profile'),
    path('forgot-password/', views.UserForgotPasswordView.as_view(), name='forgot-password'),
]
