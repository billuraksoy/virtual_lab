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
    form_model = 'player'

class Rules(Page):
    def vars_for_template(self):
        return dict(
            total_rounds = self.session.config['total_rounds'],
            group_size = self.session.config['group_size']
            )

class GameOverview(Page):
    form_model = 'player'
    form_fields = ['attention_check_1']
    def vars_for_template(self):
        return dict(
            base_tokens = self.session.config['base_tokens'],
            group_size = self.session.config['group_size'],
            total_tokens = self.session.config['base_tokens']*self.session.config['group_size'],
            inc = self.session.config['increment'],
            other_part = self.session.config['group_size']-1
            )
class GameOverview2(Page):
    form_model = 'player'
    form_fields = ['attention_check_2']
    def vars_for_template(self):
        return dict(
            threshold_high=self.session.config['threshold_high'],
            threshold_low=self.session.config['threshold_low'],
            value_high=self.session.config['value_high'],
            value_low=self.session.config['value_low']
            )


page_sequence = [
    PID_Begin,
    Informed_Consent,
    Overview,
    Rules,
    GameOverview,
    GameOverview2
]