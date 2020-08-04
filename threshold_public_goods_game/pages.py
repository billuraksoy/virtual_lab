from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class GroupWait(WaitPage):
	pass

class Game(Page):
    form_model = 'player'
    form_fields = ['contribution_acc_a','contribution_acc_b']
    def vars_for_template(self):
        return dict(
            roundNum = self.round_number
            )
    
class ResWait(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [GroupWait, Game, ResWait, Results]
