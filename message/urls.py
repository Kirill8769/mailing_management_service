from django.urls import path
from django.views.decorators.cache import cache_page

from message import views
from .apps import MessageConfig

app_name = MessageConfig.name

urlpatterns = [
    path('', cache_page(10)(views.MessageListView.as_view()), name='message_list'),
    path('detail/<int:pk>/', views.MessageDetailView.as_view(), name='message_detail'),
    path('create/', views.MessageCreateView.as_view(), name='message_create'),
    path('update/<int:pk>/', views.MessageUpdateView.as_view(), name='message_update'),
    path('delete/<int:pk>/', views.MessageDeleteView.as_view(), name='message_delete'),
]
