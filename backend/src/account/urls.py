from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import(
    RegisterView, VerifyEmailView, LoginView, LogoutView,
    RequestPasswordResetView, PasswordTokenCheckView, SetNewPasswordView
)

app_name='account'

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('verify-email/', VerifyEmailView.as_view(), name="verify-email"),
    path('login/', LoginView.as_view(), name="login"),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('request-password-reset/', RequestPasswordResetView.as_view(), name="request-password-reset"),
    path('token-check/<uid>/<token>/', PasswordTokenCheckView.as_view(), name="token-check"),
    path('set-new-password/', SetNewPasswordView.as_view(), name="set-new-password"),

]