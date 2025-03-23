from django.urls import path

from .views import embedded_reviews

urlpatterns = [
    path("entities/<uuid:entity_id>/reviews", embedded_reviews, name="embedded_reviews"),
]
