# apps/users/views.py
from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer, CustomTokenSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny


from rest_framework_simplejwt.views import TokenObtainPairView

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    # def get_permissions(self):
    #     if self.action == 'create':
    #         return [AllowAny()]
    #     return super().get_permissions()
    
class Login(TokenObtainPairView):
    serializer_class = CustomTokenSerializer
    
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user = authenticate(username=username, password=password)
        keys_to_include = ['email', 'username', 'id']
        
        if user:
            login_serializer = self.serializer_class(data=request.data)
            if login_serializer.is_valid():
                user_serializer = UserSerializer(user)
                filtered_user_data = {
                    key: user_serializer.data[key] for key in keys_to_include if key in user_serializer.data
                }
                return Response({
                    'token': login_serializer.validated_data.get('access'),
                    'refresh_token': login_serializer.validated_data.get('refresh'),
                    'user': filtered_user_data,
                    'message': 'User logged successfully',
                }, status=status.HTTP_200_OK)
        return Response({'error':'username or password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        
class Logout(GenericAPIView):
    
    def post(self, request, *args, **kwargs):
        user = User.objects.filter(id=request.data.get('user', 0))
        if user.exists():
            RefreshToken.for_user(user.first())
            return Response({'message': 'Sesión cerrada correctamente.'}, status=status.HTTP_200_OK)
        return Response({'error': 'No existe este usuario.'}, status=status.HTTP_400_BAD_REQUEST)