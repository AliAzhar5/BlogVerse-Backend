from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import CreateAPIView
from v1.accounts.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
User = get_user_model()

class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny, )
    
    def jwt_response_payload_handler(self, token, user=None, request=None):
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return {
            'access': access_token,
            'refresh': refresh_token
        }