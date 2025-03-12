from uuid import uuid4

from django.db import models
from user.models import CustomUser


class Entity(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
        unique=True,
        help_text="Unique identifier for the entity.",
    )
    title = models.CharField(max_length=255, help_text="Title of the entity.")
    description = models.TextField(
        blank=True, help_text="Detailed description of the entity."
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Timestamp when the entity was created."
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="entities",
        help_text="The service user that owns this entity.",
        default=None,
    )

    def __str__(self):
        return self.title
