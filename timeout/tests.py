from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from custom_templates.custom_classes import *

class PlayerBot(SBot):
    def play_round(self):
        s=super().snap()
        pass
