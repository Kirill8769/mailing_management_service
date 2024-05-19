from django.urls import path
from django.views.decorators.cache import cache_page

from .apps import ClientConfig
from client import views

app_name = ClientConfig.name

urlpatterns = [
    path('', views.ClientListView.as_view(), name='client_list'),
    path('detail/<int:pk>/', cache_page(60)(views.ClientDetailView.as_view()), name='client_detail'),
    path('create/', views.ClientCreateView.as_view(), name='client_create'),
    path('update/<int:pk>/', views.ClientUpdateView.as_view(), name='client_update'),
    path('delete/<int:pk>/', views.ClientDeleteView.as_view(), name='client_delete'),
]
