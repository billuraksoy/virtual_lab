from otree.api import Currency as c, currency_range
from . import *
from otree.api import Bot

from custom_templates.custom_funcs import snap

class PlayerBot(Bot):
    def play_round(self):
        #snap(self)
        yield ConsentPage
        #snap(self)
        yield Overview
        #snap(self)
        yield PageIntro
