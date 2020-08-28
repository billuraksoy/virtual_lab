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
            self.player.TreatmentVars(),
            informed_consent = self.session.config['consent']
            )

class Overview(Page):
    def vars_for_template(self):
        return self.player.TreatmentVars()

class Rules(Page):
    def vars_for_template(self):
        return self.player.TreatmentVars()

class GameOverview(Page):
    form_model = 'player'
    form_fields = ['attention_check_1']
    def vars_for_template(self):
        d = self.player.TreatmentVars()
        return dict(
            d,
            total_tokens = d['base_tokens']*d['group_size'],
            other_part = d['group_size']-1
            )

class GameOverview2(Page):
    form_model = 'player'
    form_fields = ['attention_check_2']
    def vars_for_template(self):
        return self.player.TreatmentVars()

class TotalEarnings(Page):
    def vars_for_template(self):
        return self.player.TreatmentVars()

class Question(Page):
    form_model='player'
    form_fields=['question1','question2','question3']
    def vars_for_template(self):
        return self.player.TreatmentVars()

class Message(Page):
    def vars_for_template(self):
        return self.player.TreatmentVars()

class Warning(Page):
    def vars_for_template(self):
        return self.player.TreatmentVars()

page_sequence = [
    #PID_Begin,
    Informed_Consent,
    Overview,
    Rules,
    GameOverview,
    GameOverview2,
    TotalEarnings,
    Question,
    Message,
    Warning
]