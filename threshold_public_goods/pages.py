from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from custom_templates.custom_funcs import *


class PID_Begin(Page):
    form_model = 'player'
    form_fields = ['p_ID']

    def before_next_page(self):
        self.player.participant.vars['p_id_begin'] = self.player.p_ID
        self.player.participant_vars_dump(self)

    def error_message(self, values):
        if len(values['p_ID']) !=24:
            return 'You must enter a valid 24 character Prolific ID.'

class Informed_Consent(Page):
    form_model = 'player'
    form_fields = ['consent']

    def vars_for_template(self):
        return dict(
            self.player.TreatmentVars(),
            all_vars = self.participant.vars,
            informed_consent = self.session.config['consent'],
            consent_link = self.session.config['consent_link']
            )
    def before_next_page(self):
        self.player.participant.vars['timed_out']=False
        self.player.participant.vars['groupmate_timed_out']=False
        
        self.player.participant_vars_dump(self)
        self.player.participant.vars['vars_json_dump']['id_in_session'] = self.player.participant.id_in_session
        self.player.participant.vars['vars_json_dump']['code'] = self.player.participant.code
        self.player.participant.vars['vars_json_dump']['label'] = self.player.participant.label
        d=self.player.TreatmentVars()
        if not d['simultaneous']:
            self.player.participant.vars["id"]=self.player.id_in_group%d['group_size']
        

class Overview(Page):
    def vars_for_template(self):
        return dict(self.player.TreatmentVars(), all_vars = self.participant.vars)

class Rules(Page):
    def vars_for_template(self):
        return dict(self.player.TreatmentVars(), all_vars = self.participant.vars)

class GameOverview(Page):
    form_model = 'player'
    form_fields = ['attention_check_1']
    def vars_for_template(self):
        d = self.player.TreatmentVars()
        return dict(
            d,
            all_vars = self.participant.vars,
            total_tokens = d['base_tokens']*d['group_size'],
            other_part = d['group_size']-1
            )
    def before_next_page(self):
        self.player.participant_vars_dump(self)
class GameOverview2(Page):
    form_model = 'player'
    form_fields = ['attention_check_2']
    def vars_for_template(self):
        d=self.player.TreatmentVars()
        return dict(
            d, 
            all_vars = self.participant.vars, 
            total_tokens = d['base_tokens']*d['group_size']
            )
    def before_next_page(self):
        self.player.participant_vars_dump(self)

class TotalEarnings(Page):
    def vars_for_template(self):
        return dict(self.player.TreatmentVars(), all_vars = self.participant.vars)

class ContributionDecisions(Page):
    def vars_for_template(self):
        return dict(self.player.TreatmentVars(), all_vars = self.participant.vars)

def tokenSFormat(con):#format contribution as "token" if 1, "tokens" otherwise
    ret=""+str(con)
    ret+=" token"
    if not con==1:
        ret+="s"
    return ret

class Question(Page):
    form_model='player'
    form_fields=['question1','question2','question3']
    def vars_for_template(self):
        d=self.player.TreatmentVars()
        self.player.oConA = 0#other person's contribution to group A
        self.player.oConB = d['base_tokens'] #other person's contribution to group B (always contributes all their tokens to B)
        self.player.yConB = d['threshold_low'] - self.player.oConB #you contribute the bare minimum
        self.player.yConA = (d['base_tokens'] - self.player.yConB)//2#your contribution to group A (give about half (integer division))
        self.player.yRem = d['base_tokens'] - self.player.yConB - self.player.yConA#your remaining tokens
        self.player.payOutB = d['value_low']# your payout from group B
        self.player.yPay = self.player.yRem+self.player.payOutB#your total payout

        oConAt = tokenSFormat(self.player.oConA)
        oConBt = tokenSFormat(self.player.oConB)
        yConAt = tokenSFormat(self.player.yConA)
        yConBt = tokenSFormat(self.player.yConB)
        return dict(
            self.player.TreatmentVars(),
            all_vars = self.participant.vars,
            oConAt = oConAt,
            oConBt = oConBt,
            yConAt = yConAt,
            yConBt = yConBt,
            )
    def before_next_page(self):
        self.player.participant_vars_dump(self)
class Message(Page):
    def vars_for_template(self):
        return dict(self.player.TreatmentVars(), all_vars = self.participant.vars)

class Your_role(Page):
    def vars_for_template(self):
        d=self.player.TreatmentVars()
        self.player.participant.vars["id"]=self.player.id_in_group%self.session.config['group_size']
        if self.player.participant.vars["id"] == 0:
            self.player.participant.vars["id"] = self.session.config['group_size']
        return dict(
            self.player.TreatmentVars(),
            all_vars = self.participant.vars,
            p_id=self.player.participant.vars["id"],
            )
    def is_displayed(self):
        return not self.player.TreatmentVars()['simultaneous']

class Wait(WaitPage):
    title_text="Please wait while we form your group. This should not take long."
    body_text="Please do not leave this page.\n\nOnce your group is constructed, the experiment will start immediately.\n\nIf you do not put your answers in a timely manner, you will be removed from the study."
    def is_displayed(self):
        return self.session.config['synchronous_game']
page_sequence = [
    #PID_Begin,
    Informed_Consent,
    Overview,
    Rules,
    GameOverview,
    GameOverview2,
    TotalEarnings,
    ContributionDecisions,
    Question,
    Your_role,
]
