from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from entity.controllers import get_entity_by_id
from rest_framework import status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from user.auth_methods.auth0_authentication import Auth0JWTAuthentication
from user.models import CustomUser as User

from .controllers import (
    create_review,
    delete_review,
    get_review_by_id,
    get_reviews_for_entity,
    update_review,
)
from .serializers import (
    EntityReviewSerializer,
    PaginatedEntityReviewResponseSerializer,
    ReviewSerializer,
)


class ReviewViewSet(viewsets.ViewSet):
    serializer_class = ReviewSerializer
    authentication_classes = [Auth0JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "page",
                openapi.IN_QUERY,
                description="Page number for paginated results",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "all",
                openapi.IN_QUERY,
                description="Set to 'true' to return all results without pagination",
                type=openapi.TYPE_BOOLEAN,
            ),
        ],
        responses={
            200: openapi.Response(
                description="Paginated list of reviews",
                schema=PaginatedEntityReviewResponseSerializer,
            )
        },
        security=[{"Auth0JWT": []}],
    )
    def list(self, request, entity_pk=None):
        entity = get_entity_by_id(request.user, entity_pk, is_service_id=False)
        reviews = get_reviews_for_entity(entity).order_by("-created_at")

        if request.query_params.get("all") == "true":
            serializer = EntityReviewSerializer(reviews, many=True)
            return Response(serializer.data)

        paginator = PageNumberPagination()
        paginated_reviews = paginator.paginate_queryset(reviews, request)
        serializer = EntityReviewSerializer(
            paginated_reviews, many=True, context={"request": request}
        )
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        responses={200: ReviewSerializer()},
        security=[{"Auth0JWT": []}],
    )
    def retrieve(self, _, pk=None, entity_pk=None):
        review = get_review_by_id(pk)

        if str(review.entity.id) != str(entity_pk):
            raise NotFound("Review not found for the specified entity")
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ReviewSerializer,
        responses={201: ReviewSerializer()},
        security=[{"Auth0JWT": []}],
    )
    def create(self, request, entity_pk=None):
        entity = get_entity_by_id(request.user, entity_pk, is_service_id=False)

        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = create_review(entity, request.user, serializer.validated_data)
            return Response(
                ReviewSerializer(review).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=ReviewSerializer,
        responses={200: ReviewSerializer()},
        security=[{"Auth0JWT": []}],
    )
    def update(self, request, pk=None, entity_pk=None):
        review = get_review_by_id(pk)
        if str(review.entity.id) != str(entity_pk):
            raise NotFound("Review not found for the specified entity")
        if User.objects.get(id=request.user.id) != review.user:
            raise NotFound("You can only update your own reviews")

        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            review = update_review(review, serializer.validated_data)
            return Response(ReviewSerializer(review).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={204: "No Content"},
        security=[{"Auth0JWT": []}],
    )
    def destroy(self, request, pk=None, entity_pk=None):
        review = get_review_by_id(pk)
        if str(review.entity.id) != str(entity_pk):
            raise NotFound("Review not found for the specified entity")
        if User.objects.get(id=request.user.id) != review.user:
            raise NotFound("You can only update your own reviews")

        delete_review(review)
        return Response(status=status.HTTP_204_NO_CONTENT)
