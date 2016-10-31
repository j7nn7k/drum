from unittest import TestCase

from drum.links.forms import LinkForm


class LinkFormsTests(TestCase):

    def test_valid_data(self):
        form = LinkForm({
            "title": "Test title",
            "link": "http://test.com/",
            "old_price": 22.22,
            "new_price": 20.5,
            "description": "What a good price!",
            "main_image": "http://test.com/img.jpg",
            "keywords": {},
        })
        self.assertTrue(form.is_valid())

    def test_title_may_not_be_empty(self):
        form = LinkForm({
            "title": "",
            "link": "http://test.com/",
            "old_price": 22.22,
            "new_price": 20.5,
            "description": "What a good price!",
            "main_image": "http://test.com/img.jpg",
            "keywords": {},
        })
        self.assertFalse(form.is_valid())

    def test_if_old_price_is_float(self):
        form = LinkForm({
            "title": "Test title",
            "link": "http://test.com/",
            "old_price": "STRING",
            "new_price": 0.5,
            "description": "What a good price!",
            "main_image": "http://test.com/img.jpg",
            "keywords": {},
        })
        self.assertFalse(form.is_valid())

        form = LinkForm({
            "title": "Test title",
            "link": "http://test.com/",
            "old_price": 0.5,
            "new_price": 0.5,
            "description": "What a good price!",
            "main_image": "http://test.com/img.jpg",
            "keywords": {},
        })
        self.assertTrue(form.is_valid())

    def test_if_new_price_is_float(self):
        form = LinkForm({
            "title": "Test title",
            "link": "http://test.com/",
            "old_price": 0.5,
            "new_price": "STRING",
            "description": "What a good price!",
            "main_image": "http://test.com/img.jpg",
            "keywords": {},
        })
        self.assertFalse(form.is_valid())

        form = LinkForm({
            "title": "Test title",
            "link": "http://test.com/",
            "old_price": 0.5,
            "new_price": 0.5,
            "description": "What a good price!",
            "main_image": "http://test.com/img.jpg",
            "keywords": {},
        })
        self.assertTrue(form.is_valid())