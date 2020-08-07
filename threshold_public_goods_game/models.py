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
    threshold_high = 10
    threshold_low = 6
    value_high = 10
    value_low = 7
    total_rounds = 10
    group_size = 1
    decision_timer=30
    waiting_room_lowerlimit=1
    simultaneous = 1
    base_tokens = 5
    increment = 1
    decision_timer = 30

    name_in_url = 'threshold_public_goods_game'
    players_per_group = group_size
    num_rounds = 10


class Subsession(BaseSubsession):
    def group_by_arrival_time_method(self,waiting_players):
        import random
        if(len(waiting_players)>=Constants.waiting_room_lowerlimit):
            #if you've got enough people get a random sample of them and put that into a group
            return random.sample(waiting_players,Constants.group_size)




class Group(BaseGroup):
    pass


class Player(BasePlayer):
    #we don't have to worry about a maximum value here because 
    #the page will error if the total is too high and if we
    #try to base each max off of the base_tokens - the contribution
    #to the other group then that max value is only updated when
    #a submission attempt is made on the form, which leaves you able
    #to softlock yourself out of certain contribution combinations.

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
        if(value%Constants.increment!=0):
            return 'Please only contribute in an increment of '+str(Constants.increment)+' tokens.'
        if(value<0):
            return 'You cannot contribute negative tokens'
        if(value+self.contribution_acc_b>Constants.base_tokens):
            return 'You cannot contribute more total tokens than you have'

    def contribution_acc_b_error_message(self, value):
        if(value%Constants.increment!=0):
            return 'Please only contribute in an increment of '+str(Constants.increment)+' tokens.'
        if(value<0):
            return 'You cannot contribute negative tokens'
        if(value+self.contribution_acc_a>Constants.base_tokens):
            return 'You cannot contribute more total tokens than you have'
