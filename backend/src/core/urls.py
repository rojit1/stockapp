from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('account.urls', namespace='account')),
    path('api/v1/profile/', include('user_profile.urls', namespace='profile')),
]
