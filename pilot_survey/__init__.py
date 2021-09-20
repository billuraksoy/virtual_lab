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
				label = "Please indicate the extent to which you agree or disagree with the following statement:\n\"The instructions were clear\”",
				choices = [
				[0,"Strongly Agree"],
				[1,"Agree"],
				[2,"Neither Agree nor Disagree"],
				[3,"Disagree"],
				[4,"Strongly Disagree"]
				]
			)
	about = models.StringField(
			label = "What do you think this study is about?"
		)
	unclear = models.StringField(
			label = "Is there anything unclear or confusing so far?"
		)

	figureOut = models.BooleanField(
				label = "Do you think that it is possible for the researchers to figure out exactly which items were true for you?",
				choices = [
					[True, "Yes"],
					[False, "No"]
				]
				)
	suspicion = models.BooleanField(
				label = "Do you think that it is possible for the researchers to figure out exactly which items were true for you?",
				choices = [
					[True, "Yes"],
					[False, "No"]
				]
			)
	share = models.StringField(
			label = "Is there anything else you would like share with the researchers?"
		)



# PAGES
class Impressions1(Page):
    form_model = 'player'
    form_fields = ['clearInstructions','about','unclear']

class Impressions2(Page):
    form_model = 'player'
    form_fields = ['figureOut','suspicion','share']

page_sequence = [Impressions1, Impressions2]
