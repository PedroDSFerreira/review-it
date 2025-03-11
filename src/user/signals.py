import os

from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from user.models import APIToken

User = get_user_model()


@receiver(post_migrate)
def create_default_users(sender, **kwargs):
    if sender.name != "user":
        return

    ADMIN_USERNAME = os.getenv("DEFAULT_ADMIN_USERNAME", "admin")
    ADMIN_EMAIL = os.getenv("DEFAULT_ADMIN_EMAIL", "admin@admin.com")
    ADMIN_PASSWORD = os.getenv("DEFAULT_ADMIN_PASSWORD", "admin")
    SERVICE_USERNAME = os.getenv("DEFAULT_SERVICE_USERNAME", "service")

    admin_user, created = User.objects.update_or_create(
        username=ADMIN_USERNAME,
        user_type="admin",
        defaults={"email": ADMIN_EMAIL, "is_superuser": True, "is_staff": True},
    )
    if created:
        admin_user.set_password(ADMIN_PASSWORD)
        admin_user.save()
        print(f"Admin user '{ADMIN_USERNAME}' created.")

    service_user, _ = User.objects.update_or_create(
        username=SERVICE_USERNAME,
        user_type="service",
        defaults={"is_staff": False, "is_superuser": False},
    )

    if not APIToken.objects.filter(user=service_user).exists():
        api_token = APIToken.objects.create(user=service_user)
        print(f"Service API token created: {api_token.key}")
