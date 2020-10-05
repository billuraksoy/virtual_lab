from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random

class Practice(Page):
    pass
class Game(Page):
    # def get_timeout_seconds(self):
    #     return self.session.config['decision_timer']
    form_model = 'player'
    form_fields = ['contribution_acc_a','contribution_acc_b']

    def before_next_page(self):
        self.player.participant_vars_dump(self)

    def vars_for_template(self):
        return dict( 
            self.player.TreatmentVars(), 
            roundNum = self.round_number
            )

    def error_message(self, values): # entry checking
        d=self.player.TreatmentVars()
        if values['contribution_acc_a'] < 0 or values['contribution_acc_b'] < 0:
            return 'You cannot contribute negative tokens.'
        if values['contribution_acc_a'] + values['contribution_acc_b'] > d['base_tokens']:
            return 'You cannot contribute more tokens than you have.'

#Use what we've coded so far for the game as a parent class and create childclasses for it.
class p1Game(Game):
    template_name = 'threshold_public_goods_practice/Game.html'
    def vars_for_template(self):
        return dict(
            super().vars_for_template(),
            after1="Your contributions to Group Accounts A and B (if any) will be presented to your simulated group member. Your simulated group member will ",
            afterb="observe your contribution behavior",
            after2=" and then make their own contribution decision.",
            group_a_con="",
            group_b_con="",
            display_contributions = 0,
            )
    def is_displayed(self):
        return not self.session.config['simultaneous'] and self.player.participant.vars["id"]==1

class p2Game(Game):
    template_name = 'threshold_public_goods_practice/Game.html'
    def vars_for_template(self):
        d=self.player.TreatmentVars()
        group_a_con = random.choice(range(0,d['base_tokens']+1,d['increment']))
        group_b_con = random.choice(range(0,d['base_tokens']+1-group_a_con,d['increment']))
        self.participant.vars['practiceA'] = group_a_con
        self.participant.vars['practiceB'] = group_b_con
        return dict(
            super().vars_for_template(),
            after1="",
            afterb="Your simulated group member’s contributions to Group Accounts A and B (if any) are presented below.",
            after2="",
            group_a_con=group_a_con,
            group_b_con=group_b_con,
            display_contributions = 1,
            )
    def is_displayed(self):
        return not self.session.config['simultaneous'] and self.player.participant.vars["id"]==2

class SimGame(Game):#simultaneous
    template_name = 'threshold_public_goods_practice/Game.html'
    def vars_for_template(self):
        return dict(
            super().vars_for_template(),
            after1="",
            afterb="",
            after2="",
            group_a_con="",
            group_b_con="",
            display_contributions = 0,
            )
    def is_displayed(self):
        return self.session.config['simultaneous']

class Results(Page):
    def vars_for_template(self):
        d=self.player.TreatmentVars()
        part1 = "You will now be matched with a real player. "
        part2 = ""
        part3 = "Please click next when you are ready."
                
        # Simulate the total contributions
        groupConA = 0
        groupConB = 0
        if (not self.session.config['simultaneous']) and self.player.participant.vars["id"]==2:
        #in this case we've already shown them what their group contributed, so we need to be consistent.
            groupConA = self.participant.vars['practiceA'] + self.player.contribution_acc_a
            groupConB = self.participant.vars['practiceB'] + self.player.contribution_acc_b
        else:
            groupConA = random.choice(range(0,d['base_tokens']+1,d['increment'])) + self.player.contribution_acc_a
            groupConB = random.choice(range(0,d['base_tokens']+1-int(groupConA),d['increment'])) + self.player.contribution_acc_b
        
        w = ""
        l = "not"
        
        # calculate the amount of tokens the player has left over
        kept = d['base_tokens']-self.player.contribution_acc_a-self.player.contribution_acc_b
        
        # set up the return vars
        self.player.acc_a_total=int(groupConA)
        self.player.thresh_a_met = bool(groupConA>=d['threshold_high'])
        self.player.acc_b_total=int(groupConB)
        self.player.thresh_b_met = bool(groupConB>=d['threshold_low'])

        ht = w if groupConA>=d['threshold_high'] else l
        AEarn = d['value_high'] if groupConA>=d['threshold_high'] else 0
        lt = w if groupConB>=d['threshold_low'] else l
        BEarn = d['value_low'] if groupConB>=d['threshold_high'] else 0
        
        # save the payoff to the datasheet otherwise it's lost to the void
        self.player.payoff = kept+AEarn+BEarn

        return dict( 
            d,
            roundNum = self.round_number, 
            highText = ht, 
            lowText = lt,
            groupConA = groupConA-self.player.contribution_acc_a,
            groupConB = groupConB-self.player.contribution_acc_b,
            totConA = groupConA,
            totConB = groupConB,
            kept = kept,
            AEarn = AEarn,
            BEarn = BEarn,
            TotEarn = kept+AEarn+BEarn,
            part1=part1,
            part2=part2,
            part3=part3 
            )
class Start(Page):
    def vars_for_template(self):
        return dict( 
            self.player.TreatmentVars()
            )

page_sequence = [Practice, p1Game, p2Game, SimGame, Results, Start]
