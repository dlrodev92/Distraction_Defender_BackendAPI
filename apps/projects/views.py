from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Project
from .serializers import ProjectSerializer
from apps.tasks.serializers import TaskSerializer
from apps.tasks.models import Task

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    
    def get_queryset(self):
        # Filtra el queryset basándose en el usuario autenticado actual
        return Project.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Establece el campo de usuario con el usuario autenticado actual
        serializer.save(user=self.request.user)