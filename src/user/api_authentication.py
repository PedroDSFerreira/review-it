from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import APIToken


class APITokenAuthentication(BaseAuthentication):
    """
    Expects an HTTP header "Authorization: Token <your_token_here>".
    Only active tokens are accepted.
    """

    keyword = "Token"

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None  # No token provided

        parts = auth_header.split()
        if len(parts) != 2 or parts[0] != self.keyword:
            return None  # Incorrect format

        token = parts[1]
        try:
            token_obj = APIToken.objects.get(key=token, is_active=True)
        except APIToken.DoesNotExist:
            raise AuthenticationFailed("Invalid or inactive API token.")

        return (token_obj.user, token_obj)
