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
from custom_templates.custom_funcs import *

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'mtpg'
    players_per_group = None
    num_rounds = 1

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
        label="This question is to check your attention. Please select rabbit",
        initial=0,
        choices=[
            [0,'no selection'],
            [0,'dog'],
            [0,'cat'],
            [1,'rabbit']
        ])
    attention_check_2 = models.IntegerField(
        label="This question is to check your attention. Please select hello",
        initial=0,
        choices=[
            [0,'no selection'],
            [0,'bye'],
            [1,'hello'],
            [0,'good']
        ])
    question1 = models.IntegerField(
        label="Is the threshold for Group Account A met?",
        initial=-1,
        choices=[
            [-1,"No Selection"],
            [1,"Yes"],
            [0,"No"]
        ])
    def question1_error_message(self, value):
        if(value==-1):
            return "Please make sure to answer all questions. You cannot move forward without answering all of the questions correctly"
        if(value==1):
            return 'Since the total tokens contributed to Group Account A is less than its threshold, the threshold is not met.'
    question2 = models.IntegerField(
        label="Is the threshold for Group Account B met?",
        initial=-1,
        choices=[
            [-1,"No Selection"],
            [1,"Yes"],
            [0,"No"]
        ])
    def question2_error_message(self, value):
        if(value==-1):
            return "Please make sure to answer all questions. You cannot move forward without answering all of the questions correctly"
        if(value==0):
            return 'Since the total tokens contributed to Group Account B is more than or equal to its threshold, the threshold is met. Thus, you will receive 7 tokens from this account'
    question3 = models.IntegerField(
        label="What are your total earnings in this hypothetical situation?"
        )
    def question3_error_message(self,value):
        if(int(value)!=8):
            return "You have 1 token remaining from your endowment. You did not receive any tokens from Group Account A since the threshold was not met. You received 7 tokens from Group Account B since the threshold was met. Thus your earnings in this game is 1+7=8 tokens."
