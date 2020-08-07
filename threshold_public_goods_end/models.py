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
    name_in_url = 'threshold_public_goods_end'
    players_per_group = None
    num_rounds = 1
    num_rounds = 10



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    birth_year = models.IntegerField(
        min=1875,
        max=2020,
        label= "What is your year of birth?")
    gender = models.IntegerField(
        choices=[[0,'Male'],[1,'Female'],[2,'Other']],
        label="What is your gender identity?"
        )
    education = models.IntegerField(
        label="What is the highest education qualification you have attained?",
        choices=[
            [0,'Did not complete High School'],
            [1,'Graduated from High School'],
            [2,'Some College Degree'],
            [3,'Bachelor’s Degree'],
            [4,'Master’s Degree'],
            [5,'Ph.D. or higher']
        ]
        )
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
    ethnicity = models.IntegerField(
        label="What is your ethnicity?",
        choices=[
            [0,'White'],
            [1,'Black or African American'],
            [2,'American Indian or Alaskan Native'],
            [3,'Asian'],
            [4,'Native Hawaiian or Pacific Islander'],
            [5,'Hispanic or Latino'],
            [6,'Middle Eastern or Arab'],
            [7,'Other (please state below)']
        ]
        )
    other = models.StringField(blank=True)
