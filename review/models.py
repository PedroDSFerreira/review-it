from django.db import models

from entity.models import Entity


class Review(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, unique=True)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    rating = models.IntegerField(default=1, choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)
