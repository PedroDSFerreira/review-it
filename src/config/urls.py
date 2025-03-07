from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from entity.views import EntityViewSet
from rest_framework import permissions, routers
from review.views import ReviewViewSet

schema_view = get_schema_view(
    openapi.Info(
        title="Review-it API",
        default_version="v1",
        # description="Test description",
        contact=openapi.Contact(email="pedrodsf21@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register(r"entities", EntityViewSet, basename="entity")
router.register(r"reviews", ReviewViewSet, basename="review")

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/v1/",
        include(
            [
                path("", include(router.urls)),
                path(
                    "docs/",
                    schema_view.with_ui("swagger", cache_timeout=0),
                    name="schema-swagger-ui",
                ),
            ]
        ),
    ),
]
