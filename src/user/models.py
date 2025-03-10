import secrets

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ("admin", "Admin"),
        ("service", "Service"),
        ("user", "User"),
    )
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default="user",
        help_text="Indicates whether this user is an admin, a service, or a client.",
    )
    jwt_sub = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Unique user identifier for mapping JWT tokens.",
    )


class APITokenManager(models.Manager):
    def authenticate(self, token_key):
        """
        Return the associated service user if the token key is valid,
        active, and belongs to a user with user_type 'service'.
        """
        try:
            token = self.get(key=token_key, is_active=True)
        except APIToken.DoesNotExist:
            return None
        if token.user.user_type != "service":
            return None
        return token.user


User = get_user_model()


class APIToken(models.Model):
    """
    Stores API tokens for service users.
    Only service users (user_type == "service") can have tokens.
    """

    key = models.CharField(max_length=40, primary_key=True, editable=False)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="api_tokens"
    )
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    objects = APITokenManager()

    def save(self, *args, **kwargs):
        if self.user.user_type != "service":
            raise ValueError("Only service users can have API tokens.")
        if not self.key:
            self.key = self.generate_key()
        super().save(*args, **kwargs)

    def generate_key(self):
        return secrets.token_hex(20)

    def __str__(self):
        return self.key
