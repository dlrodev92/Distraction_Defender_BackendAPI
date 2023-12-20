# tasks/models.py
from django.db import models
from apps.projects.models import Project

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    label = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name