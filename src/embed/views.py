from django.core.paginator import Paginator
from django.shortcuts import render

from config.settings import REST_FRAMEWORK
from review.controllers import get_reviews_for_entity


def embedded_reviews(request, entity_id):
    reviews = get_reviews_for_entity(entity_id).order_by("-created_at")

    paginator = Paginator(reviews, REST_FRAMEWORK.get("PAGE_SIZE"))
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
        },
    )
