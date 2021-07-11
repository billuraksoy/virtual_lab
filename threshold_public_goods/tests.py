from otree.api import Currency as c, currency_range
from . import *
from otree.api import Bot

from custom_templates.custom_funcs import snap

class PlayerBot(Bot):
    def play_round(self):
        snap(self)
        yield Informed_Consent, dict(consent=True)
        snap(self)
        yield Overview
        snap(self)
        yield Rules
        snap(self)
        yield GameOverview, dict(attention_check_1=1)
        snap(self)
        yield GameOverview2, dict(attention_check_2=1)
        snap(self)
        yield TotalEarnings
        snap(self)
        yield ContributionDecisions
        snap(self)
        yield Question, dict(question1=0,question2=1,question3=self.player.yPay)
        snap(self)
        if not self.player.TreatmentVars()['simultaneous']:
            yield Your_role
