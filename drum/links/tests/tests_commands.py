import datetime

from django.utils import timezone
from drum.links.management.commands import expire_links
from freezegun import freeze_time
from mezzanine.utils.tests import TestCase
from django.contrib.auth.models import User
from drum.links.models import Link


@freeze_time("2016-11-06 15:00:00")
class ExpireLinksCommandTests(TestCase):
    def setUp(self):
        super(ExpireLinksCommandTests, self).setUp()
        self.user = User.objects.get(username='test')
        Link.objects.create(title="Link is expired and flagged", link="http://expiredflagged.com/", is_expired=True,
                            user=self.user, deal_expiry_date=timezone.now() - datetime.timedelta(days=5))
        Link.objects.create(title="Link is expired and NOT flagged", link="http://expirednotflagged.com/",
                            is_expired=False, user=self.user,
                            deal_expiry_date=timezone.now() - datetime.timedelta(days=5))
        Link.objects.create(title="Link is expired and NOT flagged", link="http://expirednotflagged.com/",
                            is_expired=False, user=self.user,
                            deal_expiry_date=timezone.now() - datetime.timedelta(minutes=1))
        Link.objects.create(title="Link is not expired", link="http://notexpired.com/", is_expired=False,
                            user=self.user, deal_expiry_date=timezone.now() + datetime.timedelta(days=5))

    def test_handle_should_set_correct_no_of_items_expired(self):
        self.assertEqual(1, len(Link.objects.filter(is_expired=True)))
        c = expire_links.Command()
        c.handle()
        self.assertEqual(3, len(Link.objects.filter(is_expired=True)))
