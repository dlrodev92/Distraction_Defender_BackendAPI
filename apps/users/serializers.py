from rest_framework import serializers
from apps.users.models import User
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenSerializer(TokenObtainPairSerializer):
    pass


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
        
        if not image:
            # Assign a default image path if no image provided
            user.image = 'profileImages/default-user.webp'
        else:
            processed_image = self.process_image(image)
            
            user.image = processed_image
        
        # Set the default values for other fields
        user.is_active = validated_data.get('is_active', True)
        user.is_staff = validated_data.get('is_staff', False)
        user.is_superuser = validated_data.get('is_superuser', False)
        
        if password:
            # Set the password and save the user
            user.set_password(password)
            user.save()
        return user
    
    def update(self, instance, validated_data):
        image = validated_data.pop('image', None)
        
        if image:
            processed_image = self.process_image(image)
            instance.image = processed_image
        
        # Update other fields
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.name = validated_data.get('name', instance.name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.is_superuser = validated_data.get('is_superuser', instance.is_superuser)
        
        instance.save()
        return instance
    
    # this function is used to process the image and return the path to the processed image
    def process_image(self, image_data):
        # Process the image and return the path to the processed image
        image = Image.open(image_data)
        output = BytesIO()
        image = image.resize((300, 300))
        image.save(output, format='WEBP', quality=100)
        output.seek(0)
        processed_image = InMemoryUploadedFile(output, 'ImageField', "%s.webp" % image_data.name.split('.')[0], 'image/webp', output.tell(), None)
        return processed_image