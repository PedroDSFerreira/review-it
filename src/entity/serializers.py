from django.db.models import Avg
from rest_framework import serializers
from utils.pagination import PaginatedResponseSerializer

from .models import Entity


class EntitySerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Entity
        fields = ("id", "title", "description", "created_at", "rating")
        read_only_fields = ("id", "created_at", "rating")

    def get_rating(self, obj):
        """
        Calculate the average rating from all reviews for this entity.
        Returns None if there are no reviews.
        """
        avg_rating = obj.reviews.aggregate(avg_rating=Avg("rating"))["avg_rating"]
        # Round to 2 decimal places if not None
        return round(avg_rating, 2) if avg_rating is not None else None


class PaginatedEntityResponseSerializer(PaginatedResponseSerializer):
    results = serializers.ListSerializer(child=EntitySerializer())
