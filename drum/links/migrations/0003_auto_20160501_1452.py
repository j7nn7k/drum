# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0002_add_image_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='new_price',
            field=models.DecimalField(decimal_places=2, max_digits=7, blank=True, help_text='Optional field. The new price of the product.', null=True, verbose_name='New Price'),
        ),
        migrations.AddField(
            model_name='link',
            name='old_price',
            field=models.DecimalField(decimal_places=2, max_digits=7, blank=True, help_text='Optional field. The old or regular price of the product.', null=True, verbose_name='Old Price'),
        ),
    ]
