import json

from custom_templates.custom_funcs import *
from otree import common
from otree.api import *


author = 'Your name here'
doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'timeout'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    participant_vars = models.LongStringField()


# FUNCTIONS
# PAGES
class MainPage(Page):
    @staticmethod
    def vars_for_template(player: Player):
        player.participant_vars = json.dumps(player.participant.vars['vars_json_dump'])


page_sequence = [MainPage]
