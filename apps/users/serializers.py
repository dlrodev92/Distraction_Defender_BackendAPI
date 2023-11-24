from rest_framework import serializers
from apps.users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenSerializer(TokenObtainPairSerializer):
    pass

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'name', 'last_name', 'image', 'is_active', 'is_staff', 'password','image')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8, 'max_length': 30, 'required': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        
        # Create the user without setting the password yet
        user = User.objects.create(**validated_data)
        
         # Set the default value for is_active
        validated_data.setdefault('is_active', True)
        validated_data.setdefault('is_staff', False)
        validated_data.setdefault('is_superuser', False)
        validated_data.setdefault('image', 'https://res.cloudinary.com/dy1xcx7kw/image/upload/v1623346219/Default/default-user-image.png')
        
        if password:
            # Set the password and save the user
            user.set_password(password)
            user.save()
        return user