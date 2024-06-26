from rest_framework import serializers
from apps.users.models import User
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from distraction_defender_api.image_processor.image_processor import process_image


class CustomTokenSerializer(TokenObtainPairSerializer):
   def validate(self, attrs):
        data = super().validate(attrs)

        # Get the user object from the validated data
        user = self.user
        
        # Customize the token payload with additional data
        data['user_id'] = user.id  

        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'name', 'last_name', 'image', 'is_active', 'is_staff', 'password')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8, 'max_length': 30, 'required': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        image = validated_data.pop('image', None)  # Get the image data if provided
        
        
        # Create the user without setting the password yet
        user = User.objects.create(**validated_data)
        
        # Set the default values for other fields
        user.is_active = True
        user.is_staff = False
        user.is_superuser =  False
        
        if not image:
            # Assign a default image path if no image provided
            user.image = 'profileImages/default-user.webp'
        else:
            processed_image = process_image(image)
            
            
            user.image = processed_image
            
            
        
        if password:
            # Set the password and save the user
            user.set_password(password)
            user.save()
        return user
    
    def update(self, instance, validated_data):
        image = validated_data.get('image')
        if image:
            processed_image = process_image(image)
            instance.image = processed_image

        # Update username
        instance.username = validated_data.get('username', instance.username)
        

        # Update password
        password = validated_data.get('password')
        if password:
            instance.set_password(password)

        instance.save()
        return instance
    
    
   