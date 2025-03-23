from rest_framework.exceptions import NotFound, PermissionDenied

from .models import Entity


def create_entity(user, validated_data):
    return Entity.objects.create(user=user, **validated_data)


def update_entity(user, entity, validated_data):
    if entity.user != user:
        raise PermissionDenied("You do not have permission to update this entity.")

    for attr, value in validated_data.items():
        setattr(entity, attr, value)
    entity.save()
    return entity


def delete_entity(user, entity):
    if entity.user != user:
        raise PermissionDenied("You do not have permission to delete this entity.")
    entity.delete()


def get_entity_by_id(entity_id):
    try:
        entity = Entity.objects.get(id=entity_id)
        return entity
    except Entity.DoesNotExist:
        raise NotFound("Entity not found")


def get_entities(user):
    return Entity.objects.filter(user=user)
