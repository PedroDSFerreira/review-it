from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render
from rest_framework.exceptions import AuthenticationFailed
from review.controllers import get_reviews_for_entity
from user.auth_methods.auth0_authentication import Auth0JWTAuthentication


def embedded_reviews(request, entity_id):
    token = request.GET.get("token")
    user_payload = None

    if token:
        request.META["HTTP_AUTHORIZATION"] = f"Bearer {token}"
        auth = Auth0JWTAuthentication()
        try:
            _, payload = auth.authenticate(request)
            user_payload = payload
        except AuthenticationFailed as e:
            return render(request, "error.html", {"message": str(e)})

    reviews = get_reviews_for_entity(entity_id).order_by("-created_at")

    paginator = Paginator(reviews, settings.REST_FRAMEWORK.get("PAGE_SIZE"))
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "reviews.html",
        {
            "reviews": page_obj,
            "iterator": range(1, 6),
            "page_obj": page_obj,
            "entity_id": entity_id,
            "auth_token": token,
            "user": user_payload,
        },
    )
