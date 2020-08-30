from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Survey(Page):
	form_model = 'player'
	form_fields=['birth_year','gender','income','ethnicity','other','major']
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
			PayingRound="Because your partner disconnected and since we need an even number of subjects for this study, you have been removed from the study pool but will be payed as if you achieved the maximum score."
			TokensEarned="5"
			ME=5
		else:
			random.seed(self.player.birth_year*(1+self.player.gender)*(1+self.player.income))
			num_paying_rounds=1
			rounds = self.participant.vars['GameRounds']
			if(num_paying_rounds>1):
				PayingRound="Rounds chosen for payment:"
				TokensEarned="in these rounds: "
				payRounds = random.sample(range(1,d['total_rounds']),num_paying_rounds)
				ME=0
				for pRound in payRounds:
					ME+=rounds[pRound]
					PayingRound+=" "+str(pRound)
					TokensEarned+=" "+str(rounds[pRound])
			else:
				PayingRound="Round chosen for payment: "
				TokensEarned="in this round: "
				payRound = random.choice(range(1,d['total_rounds']))
				PayingRound+=str(payRound)
				TokensEarned+=str(rounds[payRound])
				ME=rounds[payRound]
		self.player.payoff=ME+self.session.config['participation_payment']
		return dict(
			d,
			PayingRound=PayingRound,
			TokensEarned=TokensEarned,
			MoneyEarned=ME,
			TotalEarnings=ME+self.session.config['participation_payment']
			)


page_sequence = [Survey, Paypal, Survey2, Summary]
