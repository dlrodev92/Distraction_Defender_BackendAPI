from rest_framework import serializers
from apps.projects.models import Project
from distraction_defender_api.image_processor.image_processor import process_image
from apps.tasks.serializers import TaskSerializer
from apps.tasks.models import Task

class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, required=False)

    class Meta:
        model = Project
        fields = ('id', 'user', 'title', 'description', 'image', 'tasks')
        extra_kwargs = {'user': {'read_only': True}, 'id': {'read_only': True}, }

def create(self, validated_data):
        image = validated_data.pop('image', None)

        # Create the project without setting the image yet
        project = Project.objects.create(**validated_data)

        if not image:
            # Assign a default image path if no image provided
            project.image = 'projectImages/project-DefaultImage.webp'
        else:
            processed_image = process_image(image)
            project.image.save(processed_image.name, processed_image, save=True)

        return project

def update( instance, validated_data):
        image = validated_data.get('image')
        if image:
            processed_image = process_image(image)
            instance.image.save(processed_image.name, processed_image, save=True)

        # Update title and description
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)

        instance.save()
        return instance