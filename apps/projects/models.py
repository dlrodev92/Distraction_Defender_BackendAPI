from django.db import models
from apps.users.models import User


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField('image', upload_to = 'projectImages/', null = True, blank = True)

    def __str__(self):
        return self.title