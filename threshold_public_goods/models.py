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
    
    threshold_high = 60
    threshold_low = 20
    value_high = 60
    value_low = 30
    total_rounds = 10
    group_size = 3
    decision_timer=30
    waiting_room_lowerlimit=3
    simultaneous = 1
    base_tokens = 20
    increment = 10


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    #attention check and intro 
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

    #Main game 
    currentRound = 0
    GroupACon = models.CurrencyField(min=0)
    def GroupACon_max(self):
        return 

    GroupBCon = models.CurrencyField(min=0)