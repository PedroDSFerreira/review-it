from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from user.auth_methods.api_authentication import APITokenAuthentication

from .controllers import (
    create_entity,
    delete_entity,
    get_entities,
    get_entity_by_id,
    update_entity,
)
from .serializers import EntitySerializer, PaginatedEntityResponseSerializer


class EntityViewSet(viewsets.ViewSet):
    serializer_class = EntitySerializer
    authentication_classes = [APITokenAuthentication]
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
                description="Paginated list of entities",
                schema=PaginatedEntityResponseSerializer,
            )
        },
        security=[{"APITokenAuth": []}],
    )
    def list(self, request):
        entities = get_entities()

        if request.query_params.get("all") == "true":
            serializer = EntitySerializer(entities, many=True)
            return Response(serializer.data)

        paginator = PageNumberPagination()
        paginated_entities = paginator.paginate_queryset(entities, request)
        serializer = EntitySerializer(paginated_entities, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        responses={200: EntitySerializer()},
        security=[{"APITokenAuth": []}],
    )
    def retrieve(self, _, pk=None):
        entity = get_entity_by_id(pk)
        serializer = EntitySerializer(entity)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=EntitySerializer,
        responses={201: EntitySerializer()},
        security=[{"APITokenAuth": []}],
    )
    def create(self, request):
        serializer = EntitySerializer(data=request.data)
        if serializer.is_valid():
            entity = create_entity(serializer.validated_data)
            out_serializer = EntitySerializer(entity)
            return Response(out_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=EntitySerializer,
        responses={200: EntitySerializer()},
        security=[{"APITokenAuth": []}],
    )
    def update(self, request, pk=None):
        entity = get_entity_by_id(pk)
        serializer = EntitySerializer(entity, data=request.data)
        if serializer.is_valid():
            entity = update_entity(entity, serializer.validated_data)
            out_serializer = EntitySerializer(entity)
            return Response(out_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={204: "No Content"},
        security=[{"APITokenAuth": []}],
    )
    def destroy(self, _, pk=None):
        entity = get_entity_by_id(pk)
        delete_entity(entity)
        return Response(status=status.HTTP_204_NO_CONTENT)
