from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from v1.accounts.views import UserCreateView

app_name = 'accounts'

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('login/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
