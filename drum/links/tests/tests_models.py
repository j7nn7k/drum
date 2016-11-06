import datetime

from django.utils import timezone
from freezegun import freeze_time
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


@freeze_time("2016-11-06 15:00:00")
class LinkManagerTests(TestCase):
    def setUp(self):
        super(LinkManagerTests, self).setUp()
        self.user = User.objects.get(username='test')
        Link.objects.create(title="Link is expired and flagged", link="http://expiredflagged.com/", is_expired=True,
                            user=self.user, deal_expiry_date=timezone.now() - datetime.timedelta(days=5))
        Link.objects.create(title="Link is expired and NOT flagged", link="http://expirednotflagged.com/",
                            is_expired=False, user=self.user,
                            deal_expiry_date=timezone.now() - datetime.timedelta(days=5))
        Link.objects.create(title="Link is not expired", link="http://notexpired.com/", is_expired=False,
                            user=self.user, deal_expiry_date=timezone.now() + datetime.timedelta(days=5))

    def test_due_should_return_links_nonexpired_and_before_today(self):
        self.assertEqual(1, len(Link.objects.due()))
        self.assertEqual("Link is expired and NOT flagged", Link.objects.due()[0].title)


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
