from django.db import models
from apps.users.models import User
import json

class WebList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    urls_json = models.TextField()

    def set_urls(self, urls):
        self.urls_json = json.dumps(urls)

    def get_urls(self):
        return json.loads(self.urls_json)

    def __str__(self):
        return self.title