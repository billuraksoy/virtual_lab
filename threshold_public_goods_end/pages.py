from otree.api import Currency as c, currency_range 
from ._builtin import Page, WaitPage
from .models import Constants
from custom_templates.custom_funcs import *
import json

class ThankYou(Page):
	def vars_for_template(self):
		return dict(all_vars = self.participant.vars)
class Survey(Page):
	form_model = 'player'
	form_fields=['birth_year','gender','income','Wh','Bl','Na','As','Nh','Hi','Me','OtherBool','other','risk']
	def error_message(self,values):
		lst=['Wh','Bl','Na','As','Nh','Hi','Me','OtherBool']
		error=True
		for i in lst:
			error = error and not values[i]
		if error:
			return "You must select at least one ethnicity."
	def vars_for_template(self):
		return dict(all_vars = self.participant.vars)
	def before_next_page(self):
		self.player.participant_vars_dump(self)
class Paypal(Page):
	form_model = 'player'
	form_fields=['paypal','venmo','venmo_number']
	def error_message(self, values):
		if values['paypal']==None and (values['venmo']==None or values['venmo_number']==None):
			return "You must enter identifying information for either a PayPal or a Venmo account."
	def vars_for_template(self):
		return dict(all_vars = self.participant.vars)
	def before_next_page(self):
		self.player.participant_vars_dump(self)		
class Survey2(Page):
	form_model = 'player'
	form_fields=['new_understanding','strategy','anything_else']
	def vars_for_template(self):
		return dict(all_vars = self.participant.vars)
	def before_next_page(self):
		self.player.participant_vars_dump(self)
class Summary(Page):
	def vars_for_template(self):
		import random
		d = self.player.TreatmentVars()
		#seed the rng based on a value that will remain the same on refresh
		PayingRoundP1=""
		TokensEarnedP1=""
		PayingRoundP2=""
		TokensEarnedP2=""
		TokensKeptP2=0
		ME1=0
		ME2=0
		if self.participant.vars.get('groupmate_timed_out', None)==True:
			PayingRoundP1="Because your partner disconnected and since we need an even number of subjects for this study, you have been removed from Part 1. But you will still earn 10 tokens from Part 1."
			TokensEarnedP1="10"
			ME1=10
		else:
			random.seed(self.player.birth_year*(1+self.player.gender)*(1+self.player.income))
			num_paying_rounds=1
			rounds = self.participant.vars['GameRounds']
			a_totals = self.participant.vars['a_total']
			b_totals = self.participant.vars['b_total']
			#print(rounds)
			if(num_paying_rounds>1):#as coded this only pays out multiple rounds for the first part
				TokensEarnedP1="Rounds chosen for payment:"
				TokensEarnedP1="in these rounds: "
				payRounds = random.sample(range(0,d['total_rounds']),num_paying_rounds)
				ME1=0
				for pRound in payRounds:
					ME1+=rounds[pRound]
					PayingRoundP1+=" "+str(pRound+1 )
					TokensEarnedP1+=" "+str(rounds[pRound])
					self.player.round_chosen_for_payment_P1=pRound
			else:
				PayingRoundP1="Round chosen for payment: "
				TokensEarnedP1="in this round: "
				payRound1 = random.choice(range(0,d['total_rounds']))
				PayingRoundP1+=str(payRound1+1)
				TokensEarnedP1+=str(int(rounds[payRound1]))
				ME1=rounds[payRound1]
				self.player.round_chosen_for_payment_P1=payRound1+1
				self.player.groupAThresholdMet = (a_totals[payRound1]>=d['threshold_high'])
				self.player.groupBThresholdMet = (b_totals[payRound1]>=d['threshold_low'])
				self.player.groupATotalContribution = a_totals[payRound1]
				self.player.groupBTotalContribution = b_totals[payRound1]
		#Part2
		PayingRoundP2 = str(self.player.participant.vars['keptR'])
		#The round where you recieve is stored here and may be diff to the round you kept: pl.participant.vars['recR']
		TokensKeptP2 = str(self.player.participant.vars['kept'])
		TokensEarnedP2 = str(self.player.participant.vars['rec'])
		self.player.round_chosen_for_payment_P2=self.player.participant.vars['keptR']
		ME2 = float(TokensKeptP2)*0.30+float(TokensEarnedP2)*0.30
		self.player.Part2Earnings=ME2

		self.player.payoff=float(ME1)+float(ME2)+float(self.session.config['participation_payment'])
		#JSON Append
		self.player.participant.vars['vars_json_dump']['Part1Earnings']=float(ME1)
		self.player.participant.vars['vars_json_dump']['Part2Earnings']=float(ME2)
		self.player.participant.vars['vars_json_dump']['TotalEarnings']=float(self.player.payoff)
		self.player.participant_vars=json.dumps(self.participant.vars['vars_json_dump'])
		return dict(
			d,
			all_vars = self.participant.vars,
			PayingRoundP1=PayingRoundP1,
			PayingRoundP2=PayingRoundP2,
			TokensEarnedP1=TokensEarnedP1,
			TokensEarnedP2=TokensEarnedP2,
			TokensKeptP2=TokensKeptP2,
			Part1Earnings=ME1,
			Part2Earnings=ME2,
			TotalEarnings=self.player.payoff
			)

page_sequence = [ThankYou, Survey, Paypal, Survey2, Summary]
