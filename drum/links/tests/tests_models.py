from unittest import TestCase

from django.contrib.auth.models import User
from drum.links.models import Link, Profile


class LinkModelsTests(TestCase):
    def test_has_link_field(self):
        l = Link()
        self.assertTrue(hasattr(l, 'link'))

    def test_has_rating_field(self):
        l = Link()
        self.assertTrue(hasattr(l, 'rating'))

    def test_has_comments_field(self):
        l = Link()
        self.assertTrue(hasattr(l, 'comments'))

    def test_has_new_price_field(self):
        l = Link()
        self.assertTrue(hasattr(l, 'new_price'))

    def test_has_old_price_field(self):
        l = Link()
        self.assertTrue(hasattr(l, 'old_price'))

    def test_has_main_image_field(self):
        l = Link()
        self.assertTrue(hasattr(l, 'main_image'))

    def test_has_is_expired_field(self):
        l = Link()
        self.assertTrue(hasattr(l, 'is_expired'))


class ProfileModelsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user', password="notsosecure")
        self.user.profile.website = "http://test.com/"
        self.user.profile.bio = "I have a dream"
        self.user.profile.karma = 777
        self.user.profile.save()

    def test_has_website_field(self):
        p = Profile.objects.get(user__username="user")
        self.assertEqual("http://test.com/", p.website)

    def test_has_bio_field(self):
        p = Profile.objects.get(user__username="user")
        self.assertEqual("I have a dream", p.bio)

    def test_has_bio_field(self):
        p = Profile.objects.get(user__username="user")
        self.assertEqual(777, p.karma)

    def tearDown(self):
        self.user.delete()
