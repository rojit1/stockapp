from rest_framework.urls import path
from .views import ProfileDetailView

app_name="profile"

urlpatterns = [
    path('details/', ProfileDetailView.as_view(), name="details")
]