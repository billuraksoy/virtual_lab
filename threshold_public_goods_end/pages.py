from otree.api import Currency as c, currency_range 
from ._builtin import Page, WaitPage
from .models import Constants
from custom_templates.custom_funcs import *

class ThankYou(Page):
	pass
class Survey(Page):
	form_model = 'player'
	form_fields=['birth_year','gender','income','Wh','Bl','Na','As','Nh','Hi','Me','OtherBool','other','major']
	def error_message(self,values):
		lst=['Wh','Bl','Na','As','Nh','Hi','Me','OtherBool']
		error=True
		for i in lst:
			error = error and not values[i]
		if error:
			return "You must select at least one ethnicity."
class Paypal(Page):
	form_model = 'player'
	form_fields=['paypal','venmo']
	def error_message(self, values):
		if values['paypal']==None and values['venmo']==None:
			return "You must enter identifying information for either a PayPal or a Venmo account."
class Survey2(Page):
	form_model = 'player'
	form_fields=['understanding','thoughts','strategy','suggestions']
class Summary(Page):
	def vars_for_template(self):
		import random
		d = self.player.TreatmentVars()
		#seed the rng based on a value that will remain the same on refresh
		TokensEarned=""
		PayingRound=""
		ME=0
		if self.participant.vars.get('groupmate_timed_out', None)==True:
			PayingRound="Because your partner disconnected and since we need an even number of subjects for this study, you have been removed from the study pool but will be entered as if you achieved the maximum score."
			TokensEarned="10"
			ME=10
		else:
			random.seed(self.player.birth_year*(1+self.player.gender)*(1+self.player.income))
			num_paying_rounds=1
			rounds = self.participant.vars['GameRounds']
			a_totals = self.participant.vars['a_total']
			b_totals = self.participant.vars['b_total']
			#print(rounds)
			if(num_paying_rounds>1):
				PayingRound="Rounds chosen for payment:"
				TokensEarned="in these rounds: "
				payRounds = random.sample(range(0,d['total_rounds']),num_paying_rounds)
				ME=0
				for pRound in payRounds:
					ME+=rounds[pRound]
					PayingRound+=" "+str(pRound+1 )
					TokensEarned+=" "+str(rounds[pRound])
					self.player.round_chosen_for_payment=pRound
			else:
				PayingRound="Round chosen for payment: "
				TokensEarned="in this round: "
				payRound = random.choice(range(0,d['total_rounds']))
				PayingRound+=str(payRound+1)
				TokensEarned+=str(rounds[payRound])
				ME=rounds[payRound]
				self.player.round_chosen_for_payment=payRound+1
				self.player.groupAThresholdMet = (a_totals[payRound]>=d['threshold_high'])
				self.player.groupBThresholdMet = (b_totals[payRound]>=d['threshold_low'])
				self.player.groupATotalContribution = a_totals[payRound]
				self.player.groupBTotalContribution = b_totals[payRound]

		self.player.payoff=ME+self.session.config['participation_payment']
		return dict(
			d,
			PayingRound=PayingRound,
			TokensEarned=TokensEarned,
			MoneyEarned=ME,
			TotalEarnings=ME+self.session.config['participation_payment']
			)


page_sequence = [ThankYou, Survey, Paypal, Survey2, Summary]
