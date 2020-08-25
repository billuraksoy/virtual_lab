# Generated by Django 2.2.12 on 2020-07-27 16:03

from django.db import migrations
import otree.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('threshold_public_goods', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='consent',
            field=otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, null=True, verbose_name=''),
        ),
    ]
