from uuid import uuid4

from django.db import models
from entity.models import Entity


class Review(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
        unique=True,
        help_text="Unique identifier for the review.",
    )
    entity = models.ForeignKey(
        Entity,
        on_delete=models.CASCADE,
        related_name="reviews",
        help_text="The entity associated with this review.",
    )
    title = models.CharField(max_length=255, help_text="Title of the review.")
    description = models.TextField(blank=True, help_text="Detailed review description.")
    rating = models.IntegerField(
        default=1,
        choices=[(i, i) for i in range(1, 6)],
        help_text="Rating from 1 (worst) to 5 (best).",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Timestamp when the review was created."
    )

    def __str__(self):
        return f"{self.title} ({self.rating}/5)"
