from django.test import TestCase
from user.models import CustomUser
from entity.models import Entity
from .models import Review

class ReviewModelTest(TestCase):
    def setUp(self):
        self.service_user = CustomUser.objects.create_user(username="service", password="pass", user_type="service")
        self.user = CustomUser.objects.create_user(username="user", password="pass", user_type="user")
        self.entity = Entity.objects.create(title="Entity", user=self.service_user)

    def test_create_review(self):
        review = Review.objects.create(
            entity=self.entity,
            user=self.user,
            title="Great!",
            description="Really liked it.",
            rating=5,
        )
        self.assertEqual(review.title, "Great!")
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.entity, self.entity)
        self.assertEqual(review.user, self.user)

    def test_review_only_by_user_type_user(self):
        with self.assertRaises(ValueError):
            Review.objects.create(
                entity=self.entity,
                user=self.service_user,
                title="Invalid",
                description="Should fail",
                rating=3,
            )

    def test_review_str(self):
        review = Review.objects.create(
            entity=self.entity,
            user=self.user,
            title="Nice",
            description="Nice review",
            rating=4,
        )
        self.assertIn("Nice", str(review))
        self.assertIn("4/5", str(review))
        self.assertIn(self.user.username, str(review))

    def test_review_update(self):
        review = Review.objects.create(
            entity=self.entity,
            user=self.user,
            title="Old Title",
            description="Old description",
            rating=2,
        )
        review.title = "Updated Title"
        review.description = "Updated description"
        review.rating = 5
        review.save()
        updated = Review.objects.get(id=review.id)
        self.assertEqual(updated.title, "Updated Title")
        self.assertEqual(updated.description, "Updated description")
        self.assertEqual(updated.rating, 5)

    def test_review_delete(self):
        review = Review.objects.create(
            entity=self.entity,
            user=self.user,
            title="To Delete",
            description="Will be deleted",
            rating=3,
        )
        review_id = review.id
        review.delete()
        self.assertFalse(Review.objects.filter(id=review_id).exists())