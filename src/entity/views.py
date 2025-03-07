from rest_framework import status, viewsets
from rest_framework.response import Response

from .controllers import create_entity, delete_entity, get_entity_by_id, update_entity
from .models import Entity
from .serializers import EntitySerializer


class EntityViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Entity.objects.all()
        serializer = EntitySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        entity = get_entity_by_id(pk)
        serializer = EntitySerializer(entity)
        return Response(serializer.data)

    def create(self, request):
        serializer = EntitySerializer(data=request.data)
        if serializer.is_valid():
            entity = create_entity(serializer.validated_data)
            out_serializer = EntitySerializer(entity)
            return Response(out_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        entity = get_entity_by_id(pk)
        serializer = EntitySerializer(entity, data=request.data)
        if serializer.is_valid():
            entity = update_entity(entity, serializer.validated_data)
            out_serializer = EntitySerializer(entity)
            return Response(out_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        entity = get_entity_by_id(pk)
        delete_entity(entity)
        return Response(status=status.HTTP_204_NO_CONTENT)
