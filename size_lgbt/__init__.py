from otree.api import *

c = Currency

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'size_lgbt'
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

class overview(Page):
    pass

class page1(Page):
    pass


class Results(Page):
    pass


page_sequence = [ConsentPage, overview, page1, Results]
