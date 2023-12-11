from django.db import models
from apps.users.models import User
import json

class WebList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weblists')
    title = models.CharField(max_length=255)
    urls_json = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.title