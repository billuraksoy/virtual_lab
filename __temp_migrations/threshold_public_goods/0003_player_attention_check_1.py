# Generated by Django 2.2.12 on 2020-07-27 17:52

from django.db import migrations
import otree.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('threshold_public_goods', '0002_player_consent'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='attention_check_1',
            field=otree.db.models.IntegerField(choices=[[0, 'no selection'], [0, 'dog'], [0, 'cat'], [1, 'rabbit']], null=True),
        ),
    ]
