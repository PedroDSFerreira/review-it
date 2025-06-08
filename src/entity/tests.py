from django.test import TestCase
from user.models import CustomUser
from .models import Entity

class EntityModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="service", password="pass", user_type="service")

    def test_create_entity(self):
        entity = Entity.objects.create(
            title="Test Entity",
            description="A test entity.",
            user=self.user,
        )
        self.assertEqual(entity.title, "Test Entity")
        self.assertEqual(entity.user, self.user)

    def test_entity_str(self):
        entity = Entity.objects.create(
            title="Entity String",
            description="Test __str__ method.",
            user=self.user,
        )
        self.assertEqual(str(entity), "Entity String")

    def test_entity_update(self):
        entity = Entity.objects.create(
            title="Old Title",
            description="Old description.",
            user=self.user,
        )
        entity.title = "New Title"
        entity.description = "New description."
        entity.save()
        updated = Entity.objects.get(id=entity.id)
        self.assertEqual(updated.title, "New Title")
        self.assertEqual(updated.description, "New description.")

    def test_entity_delete(self):
        entity = Entity.objects.create(
            title="To Delete",
            description="Will be deleted.",
            user=self.user,
        )
        entity_id = entity.id
        entity.delete()
        self.assertFalse(Entity.objects.filter(id=entity_id).exists())