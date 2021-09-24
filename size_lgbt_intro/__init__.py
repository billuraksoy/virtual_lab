from otree.api import *

c = Currency

doc = """
Your app description
"""

class Constants(BaseConstants):
    name_in_url = 'size_intro'
    players_per_group = None
    num_rounds = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
	pass
	
# PAGES
class ConsentPage(Page):
    pass

class Overview(Page):
    pass

class PageIntro(Page):
    pass

class Example(Page):
    form_model = 'player'
    form_fields = ['number_stated_intro']

page_sequence = [ConsentPage, Overview, PageIntro, Example]