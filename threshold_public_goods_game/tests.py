from otree.api import Currency as c, currency_range, expect
from . import pages
from ._builtin import Bot
from .models import Constants
import random
from custom_templates.custom_funcs import snap

class PlayerBot(Bot):
    def play_round(self):
        snap(self)
        d=self.player.TreatmentVars()
        
        #randomize the input so that 
        randA = random.choice(range(0, d['base_tokens'],d['increment']))
        randB = random.choice(range(0, d['base_tokens']-int(randA),d['increment']))

        if d['simultaneous']:
            yield pages.SimGame, dict(contribution_acc_a=randA,contribution_acc_b=randB)
        elif self.player.participant.vars["id"]==1:
            yield pages.p1Game, dict(contribution_acc_a=randA,contribution_acc_b=randB)
        elif self.player.participant.vars["id"]==2:
            yield pages.p2Game, dict(contribution_acc_a=randA,contribution_acc_b=randB)
        elif self.player.participant.vars["id"]==3:
            yield pages.p3Game, dict(contribution_acc_a=randA,contribution_acc_b=randB)
        #testing results
        snap(self)
        yield pages.Results
        expect(self.player.acc_a_total>=randA,True)
        expect(self.player.acc_b_total>=randB,True)
        expectedTokens = d['base_tokens']-randA-randB
        if(self.player.acc_a_total>=d['threshold_high']):
            expect(self.player.thresh_a_met, True)
            expectedTokens+=d['value_high']
        if(self.player.acc_b_total>=d['threshold_low']):
            expect(self.player.thresh_b_met, True)
            expectedTokens+=d['value_low']
        expect(self.player.payoff, expectedTokens)
