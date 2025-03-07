from django.db import models


class Entity(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
