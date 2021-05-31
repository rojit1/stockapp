from django.urls import path
from .views import DailyData

urlpatterns = [
    path('<str:symbol>/all-data/', DailyData.as_view())
]