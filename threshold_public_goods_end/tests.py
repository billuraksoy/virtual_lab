from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from custom_templates.custom_classes import *

class PlayerBot(SBot):
    def play_round(self):
        yield pages.ThankYou
        s=super().snap()
        yield pages.Survey, dict(birth_year=2020,gender=2,income=0,Wh=False,Bl=False,Na=False,As=False,Nh=False,Hi=False,Me=False,OtherBool=True,other="Bot",risk=6)
        s=super().snap()
        yield pages.Paypal, dict(paypal="non applicable",venmo="non applicable",venmo_number="NaN")
        s=super().snap()
        yield pages.Survey2, dict(new_understanding=2,strategy="No, I made decisions randomly.",anything_else="No.")
        s=super().snap()
        pass
