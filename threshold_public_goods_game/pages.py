from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class GroupWait(WaitPage):
	group_by_arrival_time=True #this triggers the group_by_arrival_time_method in the subsection class under models.py
	title_text="Please wait while we form your group. This should not take long."
	body_text="Please do not leave this page.\n\nOnce your group is constructed the experiment will start immediately.\n\nIf you do not put your answers in a timely manner, you will be removed from the study."

class Game(Page):
	timeout_seconds = Constants.decision_timer
	form_model = 'player'
	form_fields = ['contribution_acc_a','contribution_acc_b']
	
	def before_next_page(self):
		self.participant.vars['timed_out']=False
		import random
		# if you time out do the bot logic
		if self.timeout_happened:
			# pick your first contribution
			# if base_tokens = 20 and increment = 10 then the range function will return 0, 10, 20 
	    	# and random will chose between them
			A = random.choice(range(0,Constants.base_tokens+1,Constants.increment))
			# same basic principle as above but you have less tokens to work with
			B = random.choice(range(0,Constants.base_tokens+1-A,Constants.increment))
			# set the player response values
			self.player.contribution_acc_a = A
			self.player.contribution_acc_b = B
			self.participant.vars['timed_out']=True

	def vars_for_template(self):
		return dict( roundNum = self.round_number )

	def error_message(self, values): # entry checking
		if values['contribution_acc_a'] + values['contribution_acc_b'] > Constants.base_tokens:
			return 'You cannot contribute more tokens than you have.'

# class Timeout(Page):
# 	def is_displayed(self):
# 		return self.player.timed_out

class ResWait(WaitPage):
	title_text = "Please wait until everyone finishes. This should not take long."
	body_text = "Please do not leave this page."
	def app_after_this_page(self, upcoming_apps):
		if self.participant.vars['timed_out']==True: # if you've timed out, go to the timeout app and stop being here.
			print("TIME OUT")
			return upcoming_apps[-1]


class Results(Page):
    def vars_for_template(self):
    	# Calculate the total contributions for each group
    	players = self.player.group.get_players()
    	groupConA = 0
    	groupConB = 0
    	for pl in players:
    		groupConA += pl.contribution_acc_a
    		groupConB += pl.contribution_acc_b
    	
    	# Hardcoded text strings Aw=A win, Bl = B loss, etc.
    	Aw = "Threshold has been met. You earned "+str(Constants.value_high)+" tokens from Group Account A."
    	Bw = "Threshold has been met. You earned "+str(Constants.value_low)+" tokens from Group Account B."
    	Al = "Threshold has not been met. You did not earn any tokens from Group Account A."
    	Bl = "Threshold has not been met. You did not earn any tokens from Group Account B."
    	
    	# calculate the amount of tokens the player has left over
    	kept = Constants.base_tokens-self.player.contribution_acc_a-self.player.contribution_acc_b
    	
    	# set up the return vars
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
    	
    	# save the payoff to the datasheet otherwise it's lost to the void
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
