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
from otree import common 
from custom_templates.custom_funcs import *

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'mtpgg_practice'
    players_per_group=None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    
    #we don't have to worry about a maximum value here because 
    #the page will error if the total is too high and if we
    #try to base each max off of the base_tokens - the contribution
    #to the other group then that max value is only updated when
    #a submission attempt is made on the form, which leaves you able
    #to softlock yourself out of certain contribution combinations.
    pr_contribution_acc_a = models.IntegerField(
        min=0,
        initial=0,
        label = "Your Contribution"
        )
    pr_contribution_acc_b = models.IntegerField(
        min=0,
        initial=0,
        label = "Your Contribution"
        )
    pr_acc_a_total=models.IntegerField(label="")
    pr_acc_b_total=models.IntegerField(label="")
    pr_thresh_a_met = models.BooleanField(label="")
    pr_thresh_b_met = models.BooleanField(label="")
