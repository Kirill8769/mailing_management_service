from django.urls import path

from mailing import views
from .apps import MailingConfig

app_name = MailingConfig.name

urlpatterns = [
    path('', views.MailingListView.as_view(), name='mailing_list'),
    path('statistic/', views.StatisticView.as_view(), name='statistic'),
    path('detail/<int:pk>/', views.MailingDetailView.as_view(), name='mailing_detail'),
    path('create/', views.MailingCreateView.as_view(), name='mailing_create'),
    path('update/<int:pk>/', views.MailingUpdateView.as_view(), name='mailing_update'),
    path('delete/<int:pk>/', views.MailingDeleteView.as_view(), name='mailing_delete'),
    path('check_status/<int:pk>/', views.change_mailing_status, name='check_status'),
]
