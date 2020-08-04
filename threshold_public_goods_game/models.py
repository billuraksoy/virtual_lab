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

    name_in_url = 'threshold_public_goods_game'
    players_per_group = group_size
    num_rounds = 10


class Subsession(BaseSubsession):
    def creating_session(self):
        self.group_randomly()
        print(self.get_group_matrix())


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    contribution_acc_a = models.CurrencyField(
        min=0,
        initial=0,
        label = "Your Contribution"
        )
    contribution_acc_b = models.CurrencyField(
        min=0,
        initial=0,
        label = "Your Contribution"
        )
    
    def contribution_acc_a_error_message(self, value):
        if(value%10!=0):
            return 'Please only contribute in an increment of '+str(Constants.increment)+' tokens.'
        if(value<0):
            return 'You cannot contribute negative tokens'
        if(value+self.contribution_acc_b>Constants.base_tokens):
            return 'You cannot contribute more total tokens than you have'

    def contribution_acc_b_error_message(self, value):
        if(value%10!=0):
            return 'Please only contribute in an increment of '+str(Constants.increment)+' tokens.'
        if(value<0):
            return 'You cannot contribute negative tokens'
        if(value+self.contribution_acc_a>Constants.base_tokens):
            return 'You cannot contribute more total tokens than you have'
