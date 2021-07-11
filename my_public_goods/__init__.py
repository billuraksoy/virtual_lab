from otree.api import *


author = 'Your name here'
doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'my_public_goods'
    players_per_group = 3
    num_rounds = 1
    endowment = c(1000)  # c() means it's a currency
    multiplier = 2


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()


class Player(BasePlayer):
    contribution = models.CurrencyField(
        min=0, max=Constants.endowment, label="How much will you contribute?"
    )


# FUNCTIONS
def set_payoffs(group: Group):
    players = group.get_players()
    contributions = [p.contribution for p in players]
    group.total_contribution = sum(contributions)
    group.individual_share = (
        group.total_contribution * Constants.multiplier / Constants.players_per_group
    )
    for p in players:
        p.payoff = Constants.endowment - p.contribution + group.individual_share


# PAGES
class Contribute(Page):
    form_model = 'player'
    form_fields = ['contribution']


class MyPage(Page):
    pass


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'


class Results(Page):
    pass


page_sequence = [Contribute, ResultsWaitPage, Results]
