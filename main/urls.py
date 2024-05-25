from django.urls import path

from .apps import MainConfig
from main import views

app_name = MainConfig.name

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]
