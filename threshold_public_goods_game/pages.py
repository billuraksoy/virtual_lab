from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class GroupWait(WaitPage):
	group_by_arrival_time=True
	title_text="Please wait while we form your group. This should not take long."
	body_text="Please do not leave this page.\n\nOnce your group is constructed the experiment will start immediately.\n\nIf you do not put your answers in a timely manner, you will be removed from the study."

class Game(Page):
    form_model = 'player'
    form_fields = ['contribution_acc_a','contribution_acc_b']
    def vars_for_template(self):
        return dict(
            roundNum = self.round_number
            )
    def error_message(self, values):
        if values['contribution_acc_a'] + values['contribution_acc_b'] > Constants.base_tokens:
            return 'You cannot contribute more tokens than you have.'
    
class ResWait(WaitPage):
	title_text = "Please wait everyone finishes. This should not take long."
	body_text = "Please do not leave this page."


class Results(Page):
    def vars_for_template(self):
    	players = self.player.group.get_players()
    	groupConA = 0
    	groupConB = 0
    	for pl in players:
    		groupConA += pl.contribution_acc_a
    		groupConB += pl.contribution_acc_b

    	Aw = "Threshold has been met. You earned "+str(Constants.value_high)+" tokens from Group Account A."
    	Bw = "Threshold has been met. You earned "+str(Constants.value_low)+" tokens from Group Account B."
    	Al = "Threshold has not been met. You did not earn any tokens from Group Account A."
    	Bl = "Threshold has not been met. You did not earn any tokens from Group Account B."
    	
    	
    	kept = Constants.base_tokens-self.player.contribution_acc_a-self.player.contribution_acc_b
    	if(groupConA>=Constants.threshold_high):
    		ht = Aw
    		AEarn = Constants.value_high
    	else:
    		ht = Al
    		AEarn = 0
    	if(groupConB>=Constants.threshold_low):
    		lt = Bw
    		BEarn = Constants.value_low
    	else:
    		lt = Bl
    		BEarn = 0
    	
    	self.player.payoff = kept+AEarn+BEarn

    	return dict( 
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
    		TotEarn = kept+AEarn+BEarn
    		)


page_sequence = [GroupWait, Game, ResWait, Results]
