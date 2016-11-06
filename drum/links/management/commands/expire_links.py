from __future__ import unicode_literals

from django.core.management import BaseCommand
from drum.links.models import Link


class Command(BaseCommand):

    help = "Sets all links as expired if the expiry date is in the past"

    def handle(self, *args, **options):
        links = Link.objects.due()
        for l in links:
            l.is_expired = True
            l.save()
            self.stdout.write(self.style.SUCCESS("Link \"{}\" expired on {}".format(l.title, l.deal_expiry_date)))
