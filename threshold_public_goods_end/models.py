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
    name_in_url = 'mtpge'
    players_per_group = None
    num_rounds = 1
    # ch=[
    #     ['0','White'],
    #     ['1','Black or African American'],
    #     ['2','American Indian or Alaskan Native'],
    #     ['3','Asian'],
    #     ['4','Native Hawaiian or Pacific Islander'],
    #     ['5','Hispanic or Latino'],
    #     ['6','Middle Eastern or Arab'],
    #     ['7','Other (please state below)']
    # ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    birth_year = models.IntegerField(
        min=1900,
        max=2020,
        label= "What is your year of birth?")
    gender = models.IntegerField(
        choices=[[0,'Male'],[1,'Female'],[2,'Other']],
        label="What is your gender identity?"
        )
    # education = models.IntegerField(
    #     label="What is the highest education qualification you have attained?",
    #     choices=[
    #         [0,'Did not complete High School'],
    #         [1,'Graduated from High School'],
    #         [2,'Some College Degree'],
    #         [3,'Bachelor’s Degree'],
    #         [4,'Master’s Degree'],
    #         [5,'Ph.D. or higher']
    #     ]
    #     )
    income = models.IntegerField(
        label="Please select your household annual income from the options below:",
        choices=[
            [0,'less than $20,000'],
            [1,'$20,000-$39,999'],
            [2,'$40,000-$59,999'],
            [3,'$60,000-$79,999'],
            [4,'$80,000-$99,999'],
            [5,'$100,000 or more']
        ] 
        )
    def make_field(label):
        return models.BooleanField(
            label=label,
            widget=widgets.CheckboxInput,
            initial=False,
            blank=True
            )
    Wh=make_field("White")
    Bl=make_field("Black or African American")
    Na=make_field("American Indian or Alaskan Native")
    As=make_field("Asian")
    Nh=make_field("Native Hawaiian or Pacific Islander")
    Hi=make_field("Hispanic or Latino")
    Me=make_field("Middle Eastern or Arab")
    OtherBool=make_field("Other (please state below)")
    other = models.StringField(blank=True, label="")
    def other_error_message(self,value):
        if self.OtherBool and value == None:
            return 'If you select Other, you must specify in the provided field.'
    #major = models.StringField(label="Please enter your full name as it appears on Howdy to receive your bonus grade.")
    paypal = models.StringField(label="PayPal:", blank=True)
    venmo = models.StringField(label="Venmo:", blank=True)
    #understanding = models.LongStringField(label="Were the instructions easy to understand?")
    #thoughts = models.LongStringField(label="What did you think about the experiment?")
    strategy = models.LongStringField(label="Did you use a particular strategy when making your decisions?")
    #suggestions = models.LongStringField(label="Do you have any suggestions for us to improve the study?")
    anything_else = models.LongStringField(label="Is there anything else you would like to share with us?")
    new_understanding = models.IntegerField(
        label="To what extent do you agree with the following statement: \"The instructions were easy to understand\"",
        choices=[
            [0,'Strongly Agree'],
            [1,'Agree'],
            [2,'Undecided'],
            [3,'Disagree'],
            [4,'Strongly Disagree']
        ] 
        )
    round_chosen_for_payment=models.IntegerField(label="")
    groupAThresholdMet = models.BooleanField(label="")
    groupBThresholdMet = models.BooleanField(label="")
    groupATotalContribution = models.IntegerField(label="")
    groupBTotalContribution = models.IntegerField(label="")
    participant_vars = models.LongStringField()
