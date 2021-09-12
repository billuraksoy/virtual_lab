from otree.api import *

c = Currency

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'size_lgbt_survey'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # federal protection question options
    promised = models.IntegerField(
        choices=[[1, 'Yes'], [0, 'No']],
        label="Do you promise that you will answer the following question without any outside help?",
        widget=widgets.RadioSelect,
    )
    
    disability = models.BooleanField(
        label='Disability',
        widget=widgets.CheckboxInput,
        initial=False,
        blank=True)

    pol_beliefs = models.BooleanField(
        label='Political beliefs/preferences/leaning',
        widget=widgets.CheckboxInput,
        initial=False,
        blank=True)

    race = models.BooleanField(
        label='Race',
        widget=widgets.CheckboxInput,
        initial=False,
        blank=True)

    sexual_orientation = models.BooleanField(
        label='Sexual orientation',
        widget=widgets.CheckboxInput,
        initial=False,
        blank=True)

    eye_color = models.BooleanField(
        label='Eye color',
        widget=widgets.CheckboxInput,
        initial=False,
        blank=True)

    sex = models.BooleanField(
        label='Sex',
        widget=widgets.CheckboxInput,
        initial=False,
        blank=True)







# PAGES
class survey_intro(Page):
    form_model = 'player'
    form_fields = ['promised']

class survey_1(Page):
    form_model = 'player'
    form_fields = ['disability',
                   'pol_beliefs',
                   'race',
                   'sexual_orientation',
                   'eye_color',
                   'sex']


page_sequence = [survey_intro, survey_1]
