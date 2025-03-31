from django.shortcuts import get_object_or_404

from .models import Review


def create_review(entity, user, validated_data):
    return Review.objects.create(entity=entity, user=user, **validated_data)


def update_review(review, validated_data):
    for attr, value in validated_data.items():
        setattr(review, attr, value)
    review.save()
    return review


def delete_review(review):
    review.delete()


def get_review_by_id(review_id):
    return get_object_or_404(Review, id=review_id)


def get_reviews_for_entity(entity):
    return Review.objects.filter(entity=entity)
