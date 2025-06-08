from django.test import TestCase
from .models import CustomUser, APIToken

class CustomUserModelTest(TestCase):
    def test_create_user(self):
        user = CustomUser.objects.create_user(username="testuser", password="pass", user_type="user")
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.user_type, "user")

    def test_create_service_user_and_token(self):
        service_user = CustomUser.objects.create_user(username="service", password="pass", user_type="service")
        token = APIToken.objects.create(user=service_user)
        self.assertEqual(token.user, service_user)
        self.assertTrue(token.key)

    def test_create_admin_user(self):
        admin = CustomUser.objects.create_user(username="admin_test", password="pass", user_type="admin")
        self.assertEqual(admin.user_type, "admin")
        self.assertFalse(admin.is_superuser)

    def test_api_token_only_for_service_user(self):
        user = CustomUser.objects.create_user(username="notservice", password="pass", user_type="user")
        with self.assertRaises(ValueError):
            APIToken.objects.create(user=user)

    def test_api_token_str_and_generate_key(self):
        service_user = CustomUser.objects.create_user(username="service2", password="pass", user_type="service")
        token = APIToken(user=service_user)
        token.save()
        self.assertEqual(str(token), token.key)
        self.assertEqual(len(token.key), 40)

    def test_api_token_authenticate(self):
        service_user = CustomUser.objects.create_user(username="service3", password="pass", user_type="service")
        token = APIToken.objects.create(user=service_user)
        authenticated_user = APIToken.objects.authenticate(token.key)
        self.assertEqual(authenticated_user, service_user)

        # Inactive token should not authenticate
        token.is_active = False
        token.save()
        self.assertIsNone(APIToken.objects.authenticate(token.key))

        # Token for non-service user should not be assignable
        user = CustomUser.objects.create_user(username="notservice2", password="pass", user_type="user")
        bad_token = APIToken(user=service_user)
        bad_token.save()
        with self.assertRaises(ValueError):
            bad_token.user = user
            bad_token.save()

        # The token is still valid for the original service user
        self.assertEqual(APIToken.objects.authenticate(bad_token.key), service_user)