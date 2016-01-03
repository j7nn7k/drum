# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='main_image',
            field=models.CharField(help_text='We try to load an image automatically. You can also set one yourself. E.g. http://example.com/image.png', max_length=256, null=True, verbose_name='Product Image', blank=True),
        ),
    ]
