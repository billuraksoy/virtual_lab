from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'threshold_public_goods'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    p_ID = models.StringField(label='Paste your Prolific ID here')
    consent = models.BooleanField(
        initial = False,
        label = '')
    attention_check_1 = models.IntegerField(
        label="Please select rabbit",
        initial=0,
        choices=[
            [0,'no selection'],
            [0,'dog'],
            [0,'cat'],
            [1,'rabbit']
        ])
    attention_check_2 = models.IntegerField(
        label="Please select hello",
        initial=0,
        choices=[
            [0,'no selection'],
            [0,'bye'],
            [1,'hello'],
            [0,'good']
        ])