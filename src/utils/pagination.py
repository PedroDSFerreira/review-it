from rest_framework import serializers


class PaginatedResponseSerializer(serializers.Serializer):
    count = serializers.IntegerField(help_text="Total number of items")
    next = serializers.CharField(
        required=False, allow_null=True, help_text="URL to next page"
    )
    previous = serializers.CharField(
        required=False, allow_null=True, help_text="URL to previous page"
    )
    results = serializers.ListSerializer(
        child=serializers.DictField(), help_text="List of results"
    )
