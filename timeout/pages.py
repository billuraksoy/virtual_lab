from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import json

class MainPage(Page):
	def vars_for_template(self):
		self.player.participant_vars=json.dumps(self.participant.vars['vars_json_dump'])

page_sequence = [MainPage]
