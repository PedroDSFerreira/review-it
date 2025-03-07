from rest_framework import serializers

from .models import Entity


class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = ("id", "title", "description", "created_at")
        read_only_fields = ("id", "created_at")
