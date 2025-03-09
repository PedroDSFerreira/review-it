from rest_framework.exceptions import NotFound

from .models import Entity


def create_entity(validated_data):
    return Entity.objects.create(**validated_data)


def update_entity(entity, validated_data):
    for attr, value in validated_data.items():
        setattr(entity, attr, value)
    entity.save()
    return entity


def delete_entity(entity):
    entity.delete()


def get_entity_by_id(entity_id):
    try:
        return Entity.objects.get(id=entity_id)
    except Entity.DoesNotExist:
        raise NotFound("Entity not found")


def get_entities():
    return Entity.objects.all()
