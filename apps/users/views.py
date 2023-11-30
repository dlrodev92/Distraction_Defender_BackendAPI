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
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework.views import APIView


from rest_framework_simplejwt.views import TokenObtainPairView

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return super().get_permissions()
    
class Login(TokenObtainPairView):
    serializer_class = CustomTokenSerializer
    
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user = authenticate(username=username, password=password)
        keys_to_include = ['email', 'username', 'id']
        
        if user:
             # Invalidate previously issued tokens associated with the user
            tokens = OutstandingToken.objects.filter(user=user)
            for token in tokens:
                try:
                    BlacklistedToken.objects.create(token=token)
                except:
                    pass
            RefreshToken.for_user(user).blacklist()
            
            # Generate new tokens
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
            return Response({'message': 'Session is over.'}, status=status.HTTP_200_OK)
        return Response({'error': 'User does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

# token verify apiview

class VerifyTokenView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        token = request.data.get('token', '')

        if token:
            try:
                exists = OutstandingToken.objects.filter(token=token).exists()
                
                if exists:
                    return Response({'valid': True}, status=status.HTTP_200_OK)
                else:
                    return Response({'valid': False}, status=status.HTTP_401_UNAUTHORIZED)
                    
            except:
                return Response({'error': 'Token is not on the list'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Token not provided'}, status=status.HTTP_400_BAD_REQUEST)