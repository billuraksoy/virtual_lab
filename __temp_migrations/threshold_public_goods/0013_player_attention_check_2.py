# Generated by Django 2.2.12 on 2020-07-27 18:07

from django.db import migrations
import otree.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('threshold_public_goods', '0012_auto_20200727_1401'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='attention_check_2',
            field=otree.db.models.IntegerField(choices=[[0, 'no selection'], [0, 'bye'], [1, 'hello'], [0, 'good']], default=0, null=True, verbose_name='Please select hello'),
        ),
    ]
