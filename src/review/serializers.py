from rest_framework import serializers

from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    # We assume that the entity is provided via the URL,
    # so it’s not expected in the request body.
    entity = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ("id", "entity", "title", "description", "rating", "created_at")
        read_only_fields = ("id", "created_at", "entity")
