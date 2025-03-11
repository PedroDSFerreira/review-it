import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from jwt import PyJWKClient
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()


class Auth0JWTAuthentication(BaseAuthentication):
    """
    Authenticates requests using an Auth0-issued JWT.
    Expects the header: "Authorization: Bearer <token>".
    """

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None  # No token provided

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise AuthenticationFailed(
                "Invalid token format. Expected format: 'Bearer <your_jwt_token>'"
            )

        token = parts[1]

        auth0_domain = settings.AUTH0_DOMAIN
        api_audience = settings.AUTH0_API_AUDIENCE
        issuer = f"https://{auth0_domain}/"

        jwks_url = f"https://{auth0_domain}/.well-known/jwks.json"
        jwk_client = PyJWKClient(jwks_url)
        try:
            signing_key = jwk_client.get_signing_key_from_jwt(token).key
        except Exception:
            raise AuthenticationFailed("Unable to find appropriate key for token.")

        try:
            payload = jwt.decode(
                token,
                signing_key,
                algorithms=["RS256"],
                audience=api_audience,
                issuer=issuer,
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token expired.")
        except jwt.JWTClaimsError:
            raise AuthenticationFailed("Incorrect claims. Check audience and issuer.")
        except Exception:
            raise AuthenticationFailed("Unable to parse authentication token.")

        auth0_sub = payload.get("sub")
        if not auth0_sub:
            raise AuthenticationFailed("Auth0 token missing subject claim.")

        user, created = User.objects.get_or_create(
            auth0_sub=auth0_sub, defaults={"username": auth0_sub, "user_type": "user"}
        )
        return (user, payload)
