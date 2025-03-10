from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from user.models import APIToken


class APITokenAuthentication(BaseAuthentication):
    """
    Expects an HTTP header "Authorization: Token <your_token_here>".
    Only active tokens belonging to a service user are accepted.
    """

    keyword = "Token"

    def authenticate(self, request):
        token = request.headers.get("Authorization")
        if not token:
            return None

        user = APIToken.objects.authenticate(token)
        if not user:
            raise AuthenticationFailed(
                "Invalid or inactive API token, or token does not belong to a service user."
            )

        token_obj = user.api_tokens.get(key=token)
        return (user, token_obj)
