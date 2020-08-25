from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Survey(Page):
	form_model = 'player'
	form_fields = ['birth_year','gender','education','income','ethnicity','other']

class Summary(Page):
	def vars_for_template(self):
		import random
		#seed the rng based on a value that will remain the same on refresh
		random.seed(self.player.birth_year*(1+self.player.gender)*(1+self.player.education)*(1+self.player.income)*(1+self.player.ethnicity))
		num_paying_rounds=1
		rounds = self.participant.vars['GameRounds']
		if(num_paying_rounds>1):
			PayingRound="Rounds chosen for payment:"
			TokensEarned="these rounds: "
			payRounds = random.sample(range(0,Constants.num_rounds),num_paying_rounds)
			ME=0
			for pRound in payRounds:
				ME+=rounds[pRound]
				PayingRound+=" "+str(pRound)
				TokensEarned+=" "+str(rounds[pRound])
		else:
			PayingRound="Round chosen for payment: "
			TokensEarned="this round: "
			payRound = random.choice(range(0,Constants.num_rounds))
			PayingRound+=str(payRound)
			TokensEarned+=str(rounds[payRound])
			ME=rounds[payRound]
		self.player.payoff=ME+2
		return dict(
			PayingRound=PayingRound,
			TokensEarned=TokensEarned,
			MoneyEarned=ME,
			TotalEarnings=ME+2
			)


page_sequence = [Survey, Summary]
