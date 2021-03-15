from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from custom_templates.custom_classes import *

class PlayerBot(SBot):
	def play_round(self):
		yield pages.Intro
		s=super().snap()
		yield pages.Play, dict(
		input_self_1=0.00,
		input_self_2=0.00,
		input_self_3=0.00,
		input_self_4=0.00,
		input_self_5=0.00,
		input_self_6=0.00,
		input_self_7=0.00,
		input_self_8=0.00,
		input_self_9=0.00,
		input_self_10=0.00,
		input_self_11=0.00,
		input_self_12=0.00,
		input_self_13=0.00,
		input_self_14=0.00,
		input_self_15=0.00,)
		s=super().snap()
