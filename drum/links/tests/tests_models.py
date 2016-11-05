from mezzanine.utils.tests import TestCase

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

    def test_has_deal_expiry_date_field(self):
        l = Link()
        self.assertTrue(hasattr(l, 'deal_expiry_date'))


class ProfileModelsTests(TestCase):

    def setUp(self):
        super(ProfileModelsTests, self).setUp()
        self.user = User.objects.get(username='test')
        self.user.profile.website = "http://test.com/"
        self.user.profile.bio = "I have a dream"
        self.user.profile.karma = 777
        self.user.profile.save()
        self.profile = Profile.objects.get(user__username="test")

    def test_has_website_field(self):
        self.assertEqual("http://test.com/", self.profile.website)

    def test_has_bio_field(self):
        self.assertEqual("I have a dream", self.profile.bio)

    def test_has_bio_field(self):
        self.assertEqual(777, self.profile.karma)
