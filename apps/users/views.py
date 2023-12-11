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
from django.utils.decorators import method_decorator
from distraction_defender_api.middleware.decode_token_middleware import TokenDecodeMiddleware
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.views import TokenObtainPairView


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return super().get_permissions()
    
    def initialize_request(self, request, *args, **kwargs):
        # This method is called before any other methods in the viewset.
        # You can access the authenticated user through request.user here.
        return super().initialize_request(request, *args, **kwargs)
    
    @method_decorator(TokenDecodeMiddleware, name='dispatch')
    def list(self, request, *args, **kwargs):
        # Retrieve only the users that the authenticated user has permission to view
        user_info = {
            'user': UserSerializer(request.user).data
        }
        return Response(user_info)
    
    def update(self, request, *args, **kwargs):
        try:
            user_id = kwargs.get('pk') 
            
            #we get the user from the database 
            user = User.objects.get(pk=user_id)

            #we get the updated user data from the request
            updated_user = request.data

            if updated_user['current_password']:
                #first chek if the current password is correct
                if check_password(updated_user['current_password'], user.password):
                    #if the current password is correct we update the user
                    user.set_password(updated_user['new_password'])
                    
                    if updated_user['username']:
                        user.username = updated_user['username']
                    else:
                        user.username = user.username
                        
                    if 'image' in updated_user:
                        if updated_user['image'] is not None and updated_user['image'] != "":
                            processed_image = UserSerializer().process_image(updated_user['image'])
                            user.image = processed_image
                    else:
                        user.image = user.image
                    
                else:
                    return Response({'error': 'Password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Current password is required'}, status=status.HTTP_400_BAD_REQUEST)

            user.save()

            # Add any additional logic or response as needed
            return Response({'success': 'User updated successfully'}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

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
        # Obtén el token del cuerpo de la solicitud
        token = request.data.get('token', '')

        # Crea una instancia de RefreshToken
        try:
            refresh_token = RefreshToken(token)
        except Exception as e:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        # Agrega el token a la lista negra
        try:
            refresh_token.blacklist()
        except Exception as e:
            return Response({'error': 'Unable to blacklist token'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': 'Session is over.'}, status=status.HTTP_200_OK)

# token verify apiview


