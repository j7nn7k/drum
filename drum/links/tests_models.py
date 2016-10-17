from unittest import TestCase

from models import Link


class LinkTests(TestCase):

    def test_has_is_expired_field(self):
        l = Link()
        self.assertTrue(hasattr(l, 'new_price'))

    def test_has_is_expired_field(self):
        l = Link()
        self.assertTrue(hasattr(l, 'is_expired'))
