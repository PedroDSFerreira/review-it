from datetime import datetime

from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render
from entity.controllers import get_entity_by_id
from rest_framework.exceptions import AuthenticationFailed
from review.controllers import get_reviews_for_entity
from review.serializers import EntityReviewSerializer  # Import the serializer
from user.auth_methods.auth0_authentication import Auth0JWTAuthentication


def embedded_reviews(request, entity_id):
    token = request.GET.get("token")
    user_payload = None

    try:
        entity = get_entity_by_id(None, entity_id, is_service_id=False)
    except Exception as e:
        return render(request, "error.html", {"message": str(e)})

    if token:
        request.META["HTTP_AUTHORIZATION"] = f"Bearer {token}"
        auth = Auth0JWTAuthentication()
        try:
            user, payload = auth.authenticate(request)
            user_payload = payload
            request.user = user
        except AuthenticationFailed as e:
            return render(request, "error.html", {"message": str(e)})

    reviews = get_reviews_for_entity(entity_id).order_by("-created_at")

    paginator = Paginator(reviews, settings.REST_FRAMEWORK.get("PAGE_SIZE"))
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    serialized_reviews = EntityReviewSerializer(
        page_obj, many=True, context={"request": request}
    ).data

    for s_review in serialized_reviews:
        s_review["created_at"] = datetime.fromisoformat(s_review["created_at"])

    return render(
        request,
        "reviews.html",
        {
            "reviews": serialized_reviews,
            "iterator": range(1, 6),
            "page_obj": page_obj,
            "entity_id": entity_id,
            "jwt_token": token,
            "user": user_payload,
        },
    )
