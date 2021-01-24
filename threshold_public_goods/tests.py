from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):
    def play_round(self):
        yield pages.Informed_Consent, dict(consent=True)
        yield pages.Overview
        yield pages.Rules
        yield pages.GameOverview, dict(attention_check_1=1)
        yield pages.GameOverview2, dict(attention_check_2=1)
        yield pages.TotalEarnings
        yield pages.ContributionDecisions
        yield pages.Question, dict(question1=0,question2=1,question3=self.player.yPay)
        if not self.player.TreatmentVars()['simultaneous']:
        	yield pages.Your_role
