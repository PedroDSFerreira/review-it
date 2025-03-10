# user/auth_methods/auth0_authentication.py
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
    Maps the token to a local user using the auth0_sub field.
    """

    def authenticate(self, request):
        auth_header = get_authorization_header(request).split()
        if not auth_header or auth_header[0].lower() != b"bearer":
            return None

        if len(auth_header) == 1:
            raise AuthenticationFailed("Invalid token header. No credentials provided.")
        if len(auth_header) > 2:
            raise AuthenticationFailed(
                "Invalid token header. Token string should not contain spaces."
            )

        token = auth_header[1].decode("utf-8")

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
