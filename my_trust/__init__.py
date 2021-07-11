from otree.api import *


author = 'Your name here'
doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'my_trust'
    players_per_group = None
    num_rounds = 1
    endowment = c(10)
    multiplication_factor = 3


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    sent_amount = models.CurrencyField(label="How much do you want to send to participant B?")
    sent_back_amount = models.CurrencyField(label="How much do you want to send back?")


class Player(BasePlayer):
    pass


# FUNCTIONS
def sent_back_amount_choices(group: Group):
    return currency_range(c(0), group.sent_amount * Constants.multiplication_factor, c(1))


def set_payoffs(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    p1.payoff = Constants.endowment - group.sent_amount + group.sent_back_amount
    p2.payoff = group.sent_amount * Constants.multiplication_factor - group.sent_back_amount


# PAGES
class Send(Page):
    form_model = 'group'
    form_fields = ['sent_amount']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1


class SendBack(Page):
    form_model = 'group'
    form_fields = ['sent_back_amount']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2

    @staticmethod
    def vars_for_template(player: Player):
        return dict(tripled_amount=player.group.sent_amount * Constants.multiplication_factor)


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'


class WaitForP1(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [Send, WaitForP1, SendBack, ResultsWaitPage, Results]
