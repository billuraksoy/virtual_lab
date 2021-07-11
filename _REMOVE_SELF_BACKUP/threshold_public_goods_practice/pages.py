from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random

class Practice(Page):
    def vars_for_template(self):
        return dict(all_vars = self.participant.vars)
class PracticeGame(Page):
    # def get_timeout_seconds(self):
    #     return self.session.config['decision_timer']
    form_model = 'player'
    form_fields = ['pr_contribution_acc_a','pr_contribution_acc_b']

    def before_next_page(self):
        self.player.participant_vars_dump(self)

    def vars_for_template(self):
        return dict( 
            self.player.TreatmentVars(), 
            roundNum = self.round_number,
            all_vars = self.participant.vars,
            id_in_group = self.player.participant.vars.get("id",None)
            )

    def error_message(self, values): # entry checking
        d=self.player.TreatmentVars()
        if values['pr_contribution_acc_a'] < 0 or values['pr_contribution_acc_b'] < 0:
            return 'You cannot contribute negative tokens.'
        if values['pr_contribution_acc_a'] + values['pr_contribution_acc_b'] > d['base_tokens']:
            return 'You cannot contribute more tokens than you have.'

#Use what we've coded so far for the game as a parent class and create childclasses for it.
class p1Game(PracticeGame):
    template_name = 'threshold_public_goods_practice/Game.html'
    def vars_for_template(self):
        return dict(
            super().vars_for_template(),
            group_a_con="",
            group_b_con="",
            display_contributions = 0,
            )
    def is_displayed(self):
        return not self.session.config['simultaneous'] and self.player.participant.vars["id"]==1

class p2Game(PracticeGame):
    template_name = 'threshold_public_goods_practice/Game.html'
    def vars_for_template(self):
        d=self.player.TreatmentVars()
        group_a_con = random.choice(range(0,d['base_tokens']+1,d['increment']))
        group_b_con = random.choice(range(0,d['base_tokens']+1-group_a_con,d['increment']))
        #prevent reloading the page from randomizing the contribution again
        self.participant.vars['practiceA'] = self.participant.vars.get('practiceA', group_a_con)
        self.participant.vars['practiceB'] = self.participant.vars.get('practiceB', group_b_con)
        return dict(
            super().vars_for_template(),
            group_a_con=self.participant.vars['practiceA'],
            group_b_con=self.participant.vars['practiceB'],
            display_contributions = 1,
            )
    def is_displayed(self):
        return not self.session.config['simultaneous'] and self.player.participant.vars["id"]==2

class p2plusGame(PracticeGame):
    template_name = 'threshold_public_goods_practice/Game.html'
    def vars_for_template(self):
        d=self.player.TreatmentVars()
        group_a_con = random.choice(range(0, d['base_tokens']*(self.player.participant.vars["id"]-1)+1,d['increment']))
        group_b_con = random.choice(range(0, d['base_tokens']*(self.player.participant.vars["id"]-1)+1-int(group_a_con),d['increment']))
        #prevent reloading the page from randomizing the contribution again
        self.participant.vars['practiceA'] = self.participant.vars.get('practiceA', group_a_con)
        self.participant.vars['practiceB'] = self.participant.vars.get('practiceB', group_b_con)
        return dict(
            super().vars_for_template(),
            group_a_con=self.participant.vars['practiceA'],
            group_b_con=self.participant.vars['practiceB'],
            display_contributions = 1,
            )
    def is_displayed(self):
        return not self.session.config['simultaneous'] and self.player.participant.vars["id"]>2

class SimGame(PracticeGame):#simultaneous
    template_name = 'threshold_public_goods_practice/Game.html'
    def vars_for_template(self):
        return dict(
            super().vars_for_template(),
            all_vars = self.participant.vars,
            group_a_con="",
            group_b_con="",
            display_contributions = 0,
            )
    def is_displayed(self):
        return self.session.config['simultaneous']

class Results(Page):
    def vars_for_template(self):
        d=self.player.TreatmentVars()
        # Simulate the total contributions
        #make sure that these participant vars are initialized if they're not
        randA = random.choice(range(0, d['base_tokens']*(d['group_size']-1)+1,d['increment']))
        randB = random.choice(range(0, d['base_tokens']*(d['group_size']-1)+1-int(randA),d['increment']))

        #prevent reloading the page from randomizing the contribution again
        self.participant.vars['practiceA'] = self.participant.vars.get('practiceA', randA)
        self.participant.vars['practiceB'] = self.participant.vars.get('practiceB', randB)
        self.participant.vars['vars_json_dump']['PracticeGame-computer_con_A'] = self.participant.vars.get('practiceA', randA)
        self.participant.vars['vars_json_dump']['PracticeGame-computer_con_B'] = self.participant.vars.get('practiceB', randB)
        
        #set up the proper group contributions
        groupConA = self.participant.vars['practiceA'] + self.player.pr_contribution_acc_a
        groupConB = self.participant.vars['practiceB'] + self.player.pr_contribution_acc_b
                
        # calculate the amount of tokens the player has left over
        kept = d['base_tokens']-self.player.pr_contribution_acc_a-self.player.pr_contribution_acc_b
        
        # set up the return vars
        self.player.pr_acc_a_total=int(groupConA)
        self.player.pr_thresh_a_met = bool(groupConA>=d['threshold_high'])
        self.player.pr_acc_b_total=int(groupConB)
        self.player.pr_thresh_b_met = bool(groupConB>=d['threshold_low'])

        lostHigh = 0 if groupConA>=d['threshold_high'] else 1
        AEarn = d['value_high'] if self.player.pr_thresh_a_met else 0
        lostLow = 0 if groupConB>=d['threshold_low'] else 1
        BEarn = d['value_low'] if self.player.pr_thresh_b_met else 0
        
        # save the payoff to the datasheet otherwise it's lost to the void
        self.player.payoff = kept+AEarn+BEarn

        return dict( 
            d,
            all_vars = self.participant.vars,
            roundNum = self.round_number, 
            lostHigh = lostHigh, 
            lostLow = lostLow,
            groupConA = groupConA-self.player.pr_contribution_acc_a,
            groupConB = groupConB-self.player.pr_contribution_acc_b,
            totConA = groupConA,
            totConB = groupConB,
            kept = kept,
            AEarn = AEarn,
            BEarn = BEarn,
            TotEarn = kept+AEarn+BEarn,
            )
class Start(Page):
    def vars_for_template(self):
        return dict( 
            self.player.TreatmentVars(),
            all_vars = self.participant.vars
            )

page_sequence = [Practice, p1Game, p2Game, p2plusGame, SimGame, Results, Start]
