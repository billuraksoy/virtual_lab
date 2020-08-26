from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class PID_Begin(Page):
    form_model = 'player'
    form_fields = ['p_ID']

    def before_next_page(self):
        self.player.participant.vars['p_id_begin'] = self.player.p_ID

    def error_message(self, values):
        if len(values['p_ID']) !=24:
            return 'You must enter a valid 24 character Prolific ID.'

class Informed_Consent(Page):
    form_model = 'player'
    form_fields = ['consent']

    def vars_for_template(self):
        return dict(
            informed_consent = self.session.config['consent'],
            )

class Overview(Page):
    pass

class Rules(Page):
    pass

class GameOverview(Page):
    form_model = 'player'
    form_fields = ['attention_check_1']
    def vars_for_template(self):
        return dict(
            total_tokens = Constants.base_tokens*Constants.group_size,
            other_part = Constants.group_size-1
            )

class GameOverview2(Page):
    form_model = 'player'
    form_fields = ['attention_check_2']

class TotalEarnings(Page):
    pass

class Question(Page):
    form_model='player'
    form_fiels=['question1','question2','question3']

class Message(Page):
    pass

page_sequence = [
    #PID_Begin,
    Informed_Consent,
    Overview,
    Rules,
    GameOverview,
    GameOverview2,
    TotalEarnings,
    Question,
    Message
]