import datetime

from django.db import models

# Create your models here.
class IdeUser(models.Model):
    workspace_name = models.CharField(max_length=255, blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    finished = models.BooleanField(default=False)
