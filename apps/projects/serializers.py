from rest_framework import serializers
from apps.projects.models import Project
from distraction_defender_api.image_processor.image_processor import process_image

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('user','title', 'description', 'image')
        extra_kwargs = {'user': {'read_only': True}}
    
    def create(self, validated_data):
        image = validated_data.pop('image', None)
        
         # Create the user without setting the password yet
        project = Project.objects.create(**validated_data)
        
        if not image:
            # Assign a default image path if no image provided
            project.image = 'profileImages/project-DefaultImage.webp'
        else:
            processed_image = process_image(image)
            
            project.image = processed_image
        
        return project
    
    def update(self, instance, validated_data):
        image = validated_data.get('image')
        if image:
            processed_image = process_image(image)
            instance.image = processed_image

        # Update title
        instance.title = validated_data.get('title', instance.username)
        
        # Update password
        instance.description = validated_data.get('description', instance.username)

        instance.save()
        return instance
        