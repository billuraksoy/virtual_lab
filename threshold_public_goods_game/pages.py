from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class GroupWait(WaitPage):
    group_by_arrival_time=True #this triggers the group_by_arrival_time_method in the subsection class under models.py
    title_text="Please wait while we form your group. This should not take long."
    body_text="Please do not leave this page.\n\nOnce your group is constructed, the experiment will start immediately.\n\nIf you do not put your answers in a timely manner, you will be removed from the study."

class Game(Page):
    def get_timeout_seconds(self):
        return self.session.config['decision_timer']
    form_model = 'player'
    form_fields = ['contribution_acc_a','contribution_acc_b']

    def before_next_page(self):
        d=self.player.TreatmentVars()
        self.participant.vars['timed_out_round']=0
        self.player.timed_out_round=self.participant.vars['timed_out_round']
        import random
        # if you time out do the bot logic
        if self.timeout_happened:
            # pick your first contribution
            # if base_tokens = 20 and increment = 10 then the range function will return 0, 10, 20 
            # and random will chose between them
            A = random.choice(range(0,d['base_tokens']+1,d['increment']))
            # same basic principle as above but you have less tokens to work with
            B = random.choice(range(0,d['base_tokens']+1-A,d['increment']))
            # set the player response values
            self.player.contribution_acc_a = A
            self.player.contribution_acc_b = B
            self.participant.vars['timed_out']=True
            self.player.timed_out_round=self.player.round_number
            others = self.player.get_others_in_group()
            for pl in others:
                pl.participant.vars['groupmate_timed_out']=True

    def vars_for_template(self):
        return dict( 
            self.player.TreatmentVars(), 
            roundNum = self.round_number 
            )

    def error_message(self, values): # entry checking
        d=self.player.TreatmentVars()
        if values['contribution_acc_a'] + values['contribution_acc_b'] > d['base_tokens']:
            return 'You cannot contribute more tokens than you have.'

# class Timeout(Page):
#     def is_displayed(self):
#         return self.player.timed_out

class ResWait(WaitPage):
    title_text = "Please wait until everyone finishes. This should not take long."
    body_text = "Please do not leave this page."
    def app_after_this_page(self, upcoming_apps):
        if self.participant.vars.get('timed_out', None)==True: # if you've timed out, go to the timeout app and stop being here.
            self.participant.vars['timed_out_round']=self.round_number
            return upcoming_apps[-1]


class Results(Page):
    def app_after_this_page(self,upcoming_apps):
        if self.participant.vars.get('groupmate_timed_out', None)==True:
            return upcoming_apps[0]
    def vars_for_template(self):
        d=self.player.TreatmentVars()
        #handle dropping groupmates
        part1 = ""
        part2 = ""
        part3 = ""
        dropText=""
        if(self.player.round_number==self.player.TreatmentVars()['total_rounds']):
            part1="Please click NEXT."
        else:
            part1 = "You will be randomly re-matched with a "
            part2 = "different"
            part3 = " participant in the next round. Please click next when you are ready to start the next round."
        if self.participant.vars.get('groupmate_timed_out', None)==True:
            dropText="Your group member has timed out. Thus, the computer randomly made a decision on their behalf. Since we need an even number of subjects for this study, you will not be able to move forward. However, we will pay you a total of $9 for your participation today."
            part1="We are sorry for this inconvenience. Please click next to participate in our short survey and also to provide your paypal/venmo information."
            part2=""
            part3=""
                

        # Calculate the total contributions for each group
        players = self.player.group.get_players()
        groupConA = 0
        groupConB = 0
        for pl in players:
            groupConA += pl.contribution_acc_a
            groupConB += pl.contribution_acc_b
        
        # # Hardcoded text strings Aw=A win, Bl = B loss, etc.
        # Aw = "Threshold is met. You earned "+str(Constants.value_high)+" tokens from Group Account A."
        # Bw = "Threshold is met. You earned "+str(Constants.value_low)+" tokens from Group Account B."
        # Al = "Threshold has not been met. You did not earn any tokens from Group Account A."
        # Bl = "Threshold has not been met. You did not earn any tokens from Group Account B."
        w = ""
        l = "not"
        
        # calculate the amount of tokens the player has left over
        kept = d['base_tokens']-self.player.contribution_acc_a-self.player.contribution_acc_b
        
        # set up the return vars
        if(groupConA>=d['threshold_high']):
            ht = w
            AEarn = d['value_high']
        else:
            ht = l
            AEarn = 0
        
        if(groupConB>=d['threshold_low']):
            lt = w
            BEarn = d['value_low']
        else:
            lt = l
            BEarn = 0
        
        # save the payoff to the datasheet otherwise it's lost to the void
        self.player.payoff = kept+AEarn+BEarn

        return dict( 
            d,
            gDropText=dropText,
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
    def before_next_page(self):
        #If it's the last round save the data to the participant otherwise 
        #we won't be able to access it in the next app
        if(self.player.round_number==self.player.TreatmentVars()['total_rounds']):
            self.participant.vars['GameRounds']=[pl.payoff for pl in self.player.in_all_rounds()]


page_sequence = [GroupWait, Game, ResWait, Results]
