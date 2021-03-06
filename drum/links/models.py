from __future__ import unicode_literals
from drum.links.manager import LinkManager
from future.builtins import int
from re import sub, split
from operator import ior
from functools import reduce

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q, CharField, DecimalField, BooleanField, DateTimeField
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from mezzanine.accounts import get_profile_model
from mezzanine.core.models import Displayable, Ownable
from mezzanine.core.request import current_request
from mezzanine.generic.models import Rating, Keyword, AssignedKeyword
from mezzanine.generic.fields import RatingField, CommentsField

USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Link(Displayable, Ownable):
    link = models.URLField(null=True,
                           blank=(not getattr(settings, "LINK_REQUIRED", False)))
    rating = RatingField()
    comments = CommentsField()
    main_image = CharField(_("Product Image"), help_text=_(
        "We try to load an image automatically. You can also set one yourself. E.g. http://example.com/image.png"),
                           max_length=256, null=True, blank=True)
    new_price = DecimalField(_("New Price"), help_text=_(
        "Optional field. The new price of the product."), max_digits=7, decimal_places=2, null=True, blank=True)
    old_price = DecimalField(_("Old Price"), help_text=_(
        "Optional field. The old or regular price of the product."),
                             max_digits=7, decimal_places=2, null=True, blank=True)
    is_expired = BooleanField(_("Expired"), help_text=_("Indicates if the deal conditions still apply"), default=False)
    deal_expiry_date = DateTimeField(_("Expires at"), help_text=_("Optional field. The deal expires at this date"),
                                     null=True, blank=True)

    objects = LinkManager()

    def get_absolute_url(self):
        return reverse("link_detail", kwargs={"slug": self.slug})

    @property
    def domain(self):
        return urlparse(self.url).netloc

    @property
    def url(self):
        if self.link:
            return self.link
        return current_request().build_absolute_uri(self.get_absolute_url())

    def save(self, *args, **kwargs):
        keywords = []
        if not self.keywords_string and getattr(settings, "AUTO_TAG", False):
            variations = lambda word: [word,
                                       sub("^([^A-Za-z0-9])*|([^A-Za-z0-9]|s)*$", "", word),
                                       sub("^([^A-Za-z0-9])*|([^A-Za-z0-9])*$", "", word)]
            keywords = sum(map(variations, split("\s|/", self.title)), [])
        super(Link, self).save(*args, **kwargs)
        if keywords:
            lookup = reduce(ior, [Q(title__iexact=k) for k in keywords])
            for keyword in Keyword.objects.filter(lookup):
                self.keywords.add(AssignedKeyword(keyword=keyword))


@python_2_unicode_compatible
class Profile(models.Model):
    user = models.OneToOneField(USER_MODEL)
    website = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    karma = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return "%s (%s)" % (self.user, self.karma)


@receiver(post_save, sender=Rating)
@receiver(post_delete, sender=Rating)
def karma(sender, **kwargs):
    """
    Each time a rating is saved, check its value and modify the
    profile karma for the related object's user accordingly.
    Since ratings are either +1/-1, if a rating is being edited,
    we can assume that the existing rating is in the other direction,
    so we multiply the karma modifier by 2. We also run this when
    a rating is deleted (undone), in which case we just negate the
    rating value from the karma.
    """
    rating = kwargs["instance"]
    value = int(rating.value)
    if "created" not in kwargs:
        value *= -1  # Rating deleted
    elif not kwargs["created"]:
        value *= 2  # Rating changed
    content_object = rating.content_object
    if rating.user != content_object.user:
        queryset = get_profile_model().objects.filter(user=content_object.user)
        queryset.update(karma=models.F("karma") + value)
