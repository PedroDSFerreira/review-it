from rest_framework import serializers
from utils.pagination import PaginatedResponseSerializer

from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    entity = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ("id", "entity", "title", "description", "rating", "created_at")
        read_only_fields = ("id", "created_at", "entity")


class PaginatedReviewResponseSerializer(PaginatedResponseSerializer):
    results = serializers.ListSerializer(child=ReviewSerializer())
