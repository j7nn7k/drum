
from django.forms.models import modelform_factory
from django.forms import ValidationError

from drum.links.models import Link


BaseLinkForm = modelform_factory(Link, fields=["title", "link", "old_price", "new_price", "description", "main_image",
                                               "deal_expiry_date", "keywords"])


class LinkForm(BaseLinkForm):

    def clean(self):
        link = self.cleaned_data.get("link", None)
        description = self.cleaned_data.get("description", None)
        if not link and not description:
            raise ValidationError("Either a link or description is required")
        return self.cleaned_data
