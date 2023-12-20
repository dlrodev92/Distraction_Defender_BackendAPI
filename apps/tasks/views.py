from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer
from apps.projects.models import Project

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    
    def get_queryset(self):
        user_projects = Project.objects.filter(user=self.request.user)
        project_ids = user_projects.values_list('id', flat=True)
        return Task.objects.filter(project__in=project_ids)

    def create(self, request, *args, **kwargs):
        project_id = self.kwargs.get('project_pk')
        request.data['project'] = project_id
        return super().create(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        project_id = self.kwargs.get('project_pk')
        request.data['project'] = project_id
        return super().delete(request, *args, **kwargs)