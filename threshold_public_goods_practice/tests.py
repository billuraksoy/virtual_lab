from otree.api import Currency as c, currency_range, expect
from . import *
from otree.api import Bot

import random
from custom_templates.custom_funcs import snap

class PlayerBot(Bot):
    def play_round(self):
        snap(self)
        yield Practice
        d=self.player.TreatmentVars()
        
        #randomize the input so that 
        randA = random.choice(range(0, d['base_tokens'],d['increment']))
        randB = random.choice(range(0, d['base_tokens']-int(randA),d['increment']))
        if d['simultaneous']:
            yield SimGame, dict(pr_contribution_acc_a=randA,pr_contribution_acc_b=randB)
        elif self.player.participant.vars["id"]==1:
            yield p1Game, dict(pr_contribution_acc_a=randA,pr_contribution_acc_b=randB)
        elif self.player.participant.vars["id"]==2:
            yield p2Game, dict(pr_contribution_acc_a=randA,pr_contribution_acc_b=randB)
        elif self.player.participant.vars["id"]>2:
            yield p2plusGame, dict(pr_contribution_acc_a=randA,pr_contribution_acc_b=randB)
               
        #testing results
        snap(self)
        yield Results
        expect(self.player.pr_acc_a_total>=randA,True)
        expect(self.player.pr_acc_b_total>=randB,True)
        expectedTokens = d['base_tokens']-randA-randB
        if(self.player.pr_acc_a_total>=d['threshold_high']):
            expect(self.player.pr_thresh_a_met, True)
            expectedTokens+=d['value_high']
        if(self.player.pr_acc_b_total>=d['threshold_low']):
            expect(self.player.pr_thresh_b_met, True)
            expectedTokens+=d['value_low']
        expect(self.player.payoff, expectedTokens)
        
        snap(self)
        yield Start, dict()
