from django.urls import path

from message import views
from .apps import MessageConfig

app_name = MessageConfig.name

urlpatterns = [
    path('', views.MessageListView.as_view(), name='message_list'),
    path('detail/<int:pk>/', views.MessageDetailView.as_view(), name='message_detail'),
    path('create/', views.MessageCreateView.as_view(), name='message_create'),
    path('update/<int:pk>', views.MessageUpdateView.as_view(), name='message_update'),
    path('delete/<int:pk>', views.MessageDeleteView.as_view(), name='message_delete'),
]