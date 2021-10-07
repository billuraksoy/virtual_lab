from otree.api import *

c = Currency

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'p_id_begin'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    p_ID = models.StringField(label='Paste your Prolific ID here')

    def p_ID_error_message(self, value):
        if len(value) != 24:
            return "Your prolific ID must be 24 characters long."

# PAGES
class P_ID(Page):
    form_model = 'player'
    form_fields = ['p_ID']

    #  def before_next_page(self):
    #    self.player.participant.vars['p_id_begin'] = self.player.p_ID

    #def error_message(self, values):
    #    if len(values['p_ID']) !=24:
    #        return 'You must enter a valid 24 character Prolific ID.'

page_sequence = [P_ID]

