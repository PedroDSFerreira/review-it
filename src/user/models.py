import secrets

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class APIToken(models.Model):
    """
    Stores API tokens for business clients.
    Admins can create these tokens from the Django admin.
    """

    key = models.CharField(max_length=40, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="api_tokens")
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        super().save(*args, **kwargs)

    def generate_key(self):
        return secrets.token_hex(20)

    def __str__(self):
        return self.key
