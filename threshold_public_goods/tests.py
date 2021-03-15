from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from custom_templates.custom_funcs import snap

class PlayerBot(Bot):
    def play_round(self):
        snap(self)
        yield pages.Informed_Consent, dict(consent=True)
        snap(self)
        yield pages.Overview
        snap(self)
        yield pages.Rules
        snap(self)
        yield pages.GameOverview, dict(attention_check_1=1)
        snap(self)
        yield pages.GameOverview2, dict(attention_check_2=1)
        snap(self)
        yield pages.TotalEarnings
        snap(self)
        yield pages.ContributionDecisions
        snap(self)
        yield pages.Question, dict(question1=0,question2=1,question3=self.player.yPay)
        snap(self)
        if not self.player.TreatmentVars()['simultaneous']:
            yield pages.Your_role
