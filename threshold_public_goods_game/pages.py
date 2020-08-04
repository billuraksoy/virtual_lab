from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class GroupWait(WaitPage):
	pass

class Game(Page):
    form_model = 'player'
    form_fields = ['contribution_acc_a','contribution_acc_b']
    def vars_for_template(self):
        return dict(
            roundNum = self.round_number
            )
    
class ResWait(WaitPage):
    pass


class Results(Page):
    def vars_for_template(self):
    	Aw = "Threshold has been met. You earned "+str(Constants.value_high)+" tokens from Group Account A."
    	Bw = "Threshold has been met. You earned "+str(Constants.value_low)+" tokens from Group Account B."
    	Al = "Threshold has not been met. You did not earn any tokens from Group Account A."
    	Bl = "Threshold has not been met. You did not earn any tokens from Group Account B."
    	if(1):
    		ht = Aw
    	else:
    		ht = Al
    	if(1):
    		lt = Bw
    	else:
    		lt = Bl
    	return dict( 
    		roundNum = self.round_number, 
    		highText =ht, 
    		lowText = lt 
    		)


page_sequence = [GroupWait, Game, ResWait, Results]
