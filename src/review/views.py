from entity.models import Entity  # Import the related entity model
from rest_framework import status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from .controllers import (
    create_review,
    delete_review,
    get_review_by_id,
    get_reviews_for_entity,
    update_review,
)
from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ViewSet):
    """
    A ViewSet for listing, creating, retrieving, updating, and deleting reviews.
    The URL should include the entity's pk as a parameter.
    """

    def list(self, request, entity_pk=None):
        # Validate that the parent entity exists.
        try:
            entity = Entity.objects.get(id=entity_pk)
        except Entity.DoesNotExist:
            raise NotFound("Entity not found")
        reviews = get_reviews_for_entity(entity)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, entity_pk=None):
        review = get_review_by_id(pk)
        if str(review.entity.id) != str(entity_pk):
            raise NotFound("Review not found for the specified entity")
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    def create(self, request, entity_pk=None):
        # Validate that the parent entity exists.
        try:
            entity = Entity.objects.get(id=entity_pk)
        except Entity.DoesNotExist:
            raise NotFound("Entity not found")
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = create_review(entity, serializer.validated_data)
            out_serializer = ReviewSerializer(review)
            return Response(out_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, entity_pk=None):
        review = get_review_by_id(pk)
        if str(review.entity.id) != str(entity_pk):
            raise NotFound("Review not found for the specified entity")
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            review = update_review(review, serializer.validated_data)
            out_serializer = ReviewSerializer(review)
            return Response(out_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, entity_pk=None):
        review = get_review_by_id(pk)
        if str(review.entity.id) != str(entity_pk):
            raise NotFound("Review not found for the specified entity")
        delete_review(review)
        return Response(status=status.HTTP_204_NO_CONTENT)
