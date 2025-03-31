from rest_framework import serializers
from utils.pagination import PaginatedResponseSerializer

from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    entity = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ("id", "entity", "title", "description", "rating", "created_at")
        read_only_fields = ("id", "created_at", "entity")


class EntityReviewSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = (
            "id",
            "entity",
            "title",
            "description",
            "rating",
            "created_at",
            "is_owner",
        )
        read_only_fields = ("id", "created_at", "entity", "is_owner")

    def get_is_owner(self, obj):
        request = self.context.get("request")
        return request and request.user == obj.user


class PaginatedEntityReviewResponseSerializer(PaginatedResponseSerializer):
    results = serializers.ListSerializer(child=EntityReviewSerializer())
