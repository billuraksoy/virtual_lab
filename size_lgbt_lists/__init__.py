from otree.api import *

c = Currency

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'size_lgbt'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    number_stated_1 = models.IntegerField(min=0, max=4, label='Please enter the total number of statements above that apply to you:')
    number_stated_2 = models.IntegerField(min=0, max=4, label='Please enter the total number of statements above that apply to you:')

    number_stated_8 = models.IntegerField(min=0, max=10, label='Please enter the total number of statements above that apply to you:')


    sensitive_q_1 = models.IntegerField(
        choices=[[1, 'Yes'], [0, 'No']],
        label="SensitiveQuestion11?",
        widget=widgets.RadioSelect,
    )

    sensitive_q_2 = models.IntegerField(
        choices=[[1, 'Yes'], [0, 'No']],
        label="SensitiveQuestion12?",
        widget=widgets.RadioSelect,
    )

    sensitive_q_8 = models.IntegerField(
        choices=[[1, 'Yes'], [0, 'No']],
        label="Have you ever travelled outside the country where you currently reside?",
        widget=widgets.RadioSelect,
    )
    promised = models.IntegerField(
        choices=[[1, 'Yes'], [0, 'No']],
        label="Do you promise that you will answer the following question without any outside help?",
        widget=widgets.RadioSelect,
    )

    # federal protection question options
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
class ConsentPage(Page):
    pass

class overview(Page):
    pass

class page_intro(Page):
    pass

class list_1(Page):
    form_model = 'player'
    form_fields = ['number_stated_1','sensitive_q_1']


class list_2(Page):
    form_model = 'player'
    form_fields = ['number_stated_2','sensitive_q_2']


class list_8(Page):
    form_model = 'player'
    form_fields = ['number_stated_8','sensitive_q_8']

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


page_sequence = [ConsentPage, overview, page_intro, list_1, list_2, list_8,survey_intro, survey_1]
