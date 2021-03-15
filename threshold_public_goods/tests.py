from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from custom_templates.custom_classes import *

class PlayerBot(SBot):
    def play_round(self):
        s=super().snap()
        yield pages.Informed_Consent, dict(consent=True)
        s=super().snap()
        yield pages.Overview
        s=super().snap()
        yield pages.Rules
        s=super().snap()
        yield pages.GameOverview, dict(attention_check_1=1)
        s=super().snap()
        yield pages.GameOverview2, dict(attention_check_2=1)
        s=super().snap()
        yield pages.TotalEarnings
        s=super().snap()
        yield pages.ContributionDecisions
        s=super().snap()
        yield pages.Question, dict(question1=0,question2=1,question3=self.player.yPay)
        s=super().snap()
        if not self.player.TreatmentVars()['simultaneous']:
            yield pages.Your_role
            s=super().snap()
