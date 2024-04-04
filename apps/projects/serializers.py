from rest_framework import serializers
from apps.projects.models import Project
from distraction_defender_api.image_processor.image_processor import process_image
from apps.tasks.serializers import TaskSerializer

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

        if image:
            image_url = process_image(image)
            project.image = image_url  # Directly save the URL
        else:
            project.image = 'https://www.eclosio.ong/wp-content/uploads/2018/08/default.png'

        project.save()
        return project

    def update(self, instance, validated_data):
        image = validated_data.get('image')
        if image:
            image_url = process_image(image)
            instance.image = image_url  # Directly save the URL

        # Update title and description
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)

        instance.save()
        return instance