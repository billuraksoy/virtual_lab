from otree.api import *


doc = """
Your app description
"""


class Constants(BaseConstants):
	name_in_url = 'pilot_survey'
	players_per_group = None
	num_rounds = 1


class Subsession(BaseSubsession):
	pass


class Group(BaseGroup):
	pass


class Player(BasePlayer):
	clearInstructions = models.IntegerField(
				label = "Please indicate the extent to which you agree or disagree with the following statement:\n\"The instructions were clear”",
				choices = [
				[0,"Strongly Agree"],
				[1,"Agree"],
				[2,"Neither Agree nor Disagree"],
				[3,"Disagree"],
				[4,"Strongly Disagree"]
				],
				widget=widgets.RadioSelect,
			)
	about = models.LongStringField(
			label = "What do you think this study is about?"
		)
	unclear = models.LongStringField(
			label = "Is there anything unclear or confusing with the study? Please explain which specific parts of the instructions were unclear or confusing to you."
		)

	figureOut = models.BooleanField(
				label = "Do you think that it is possible for the researchers to figure out exactly which individual statements were true for you?",
				choices = [
					[True, "Yes"],
					[False, "No"]
				]
				)
	#suspicion = models.BooleanField(
	#			label = "When providing your answers in the study, did you suspect that researchers may know a way to know exactly which individual statements were true for you?",
	#			choices = [
	#				[True, "Yes"],
	#				[False, "No"]
	#			]
	#		)


	figureOut_share = models.LongStringField(
			label = "Please explain why you think it is possible/impossible for the researchers to figure out exactly which individual statements were true for you."
		)


# PAGES
class Impressions1(Page):
    form_model = 'player'
    form_fields = ['clearInstructions','about','unclear']

class Impressions2(Page):
    form_model = 'player'
    form_fields = ['figureOut','figureOut_share']

class Impressions3(Page):
	pass

page_sequence = [Impressions1, Impressions2,Impressions3]
