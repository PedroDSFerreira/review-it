from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from user.models import APIToken

User = get_user_model()


@receiver(post_migrate)
def create_default_users(sender, **kwargs):
    if sender.name != "user":
        return

    ADMIN_USERNAME = "admin"
    ADMIN_EMAIL = "admin@example.com"
    ADMIN_PASSWORD = "adminpassword"
    SERVICE_USERNAME = "service_account"

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
