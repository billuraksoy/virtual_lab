from otree.api import Currency as c, currency_range
from . import *
from otree.api import Bot

from custom_templates.custom_funcs import snap

class PlayerBot(Bot):
    def play_round(self):
        snap(self)
        yield ThankYou
        snap(self)
        yield Survey, dict(birth_year=2020,gender=2,income=0,Wh=False,Bl=False,Na=False,As=False,Nh=False,Hi=False,Me=False,OtherBool=True,other="Bot",risk=6)
        snap(self)
        yield Paypal, dict(paypal="non applicable",venmo="non applicable",venmo_number="NaN")
        snap(self)
        yield Survey2, dict(new_understanding=2,strategy="No, I made decisions randomly.",anything_else="No.")
        snap(self)
        pass
