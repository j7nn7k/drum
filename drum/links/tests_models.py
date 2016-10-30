from unittest import TestCase

from models import Link


class LinkModelsTests(TestCase):

    def test_has_new_price_field(self):
        l = Link()
        self.assertTrue(hasattr(l, 'new_price'))

    def test_has_old_price_field(self):
        l = Link()
        self.assertTrue(hasattr(l, 'old_price'))

    def test_has_main_image_field(self):
        l = Link()
        self.assertTrue(hasattr(l, 'main_image'))
