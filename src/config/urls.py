from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from entity.views import EntityViewSet
from rest_framework import permissions, routers
from rest_framework_nested.routers import NestedDefaultRouter
from review.views import ReviewViewSet

openapi_info = openapi.Info(
    title="Review-it API",
    default_version="v1",
    description="A review platform for businesses",
    contact=openapi.Contact(email="pedrodsf21@gmail.com"),
    license=openapi.License(name="MIT License"),
)
schema_view = get_schema_view(
    openapi_info, public=True, permission_classes=(permissions.AllowAny,)
)


router = routers.DefaultRouter()
router.register(r"entities", EntityViewSet, basename="entity")

entity_router = NestedDefaultRouter(router, r"entities", lookup="entity")
entity_router.register(r"reviews", ReviewViewSet, basename="entity-reviews")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(router.urls)),
    path("api/v1/", include(entity_router.urls)),
    path(
        "api/v1/docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
