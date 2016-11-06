from django.utils import timezone
from mezzanine.core.managers import DisplayableManager


class LinkManager(DisplayableManager):

    def due(self):
        l = self.model.objects.exclude(is_expired=True).filter(deal_expiry_date__lt=timezone.now())
        return l
