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
            informed_consent = self.session.config['consent']
            )
    def before_next_page(self):
        self.player.participant.vars['timed_out']=False
        self.player.participant.vars['groupmate_timed_out']=False
        d=self.player.TreatmentVars()
        if not d['simultaneous']:
            self.player.participant.vars["id"]=self.player.id_in_group%d['group_size']
        self.player.participant_vars_dump(self)

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
    def before_next_page(self):
        self.player.participant_vars_dump(self)
class GameOverview2(Page):
    form_model = 'player'
    form_fields = ['attention_check_2']
    def vars_for_template(self):
        return self.player.TreatmentVars()

class TotalEarnings(Page):
    def vars_for_template(self):
        return self.player.TreatmentVars()

class ContributionDecisions(Page):
    def vars_for_template(self):
        return self.player.TreatmentVars()

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
            oConAt = oConAt,
            oConBt = oConBt,
            yConAt = yConAt,
            yConBt = yConBt,
            )
    def before_next_page(self):
        self.player.participant_vars_dump(self)
class Message(Page):
    def vars_for_template(self):
        return self.player.TreatmentVars()

class Your_role(Page):
    def vars_for_template(self):
        d=self.player.TreatmentVars()
        #predeclare the variables we'll use for the dict so their scope isn't limited to the if statements
        mover_title = ""
        pt1 = ""
        italics = ""
        bold = ""
        pt2 = ""
        if not d['simultaneous']:
            pt1 = "You are the "
            if self.player.id_in_group%2 == 1:
                self.player.participant.vars["id"]=1
                mover_title = "You Have Been Randomly Selected to be the First Mover"
                italics = "first mover"
                pt2 = ". This means you will always make your decision first. And then, you group member will observe your decisions and make their own decision. At the end of each round, you will be provided a round summary screen where we provide information about contributions to the group accounts and your earnings in that round. After reading information provided in these summary screens, do not forget to click next in a timely manner. This will prevent delays in the experiment."
            elif self.player.id_in_group%2 == 0:
                self.player.participant.vars["id"]=2
                mover_title = "You are Randomly Selected to be the Second Mover"
                italics = "second mover"
                pt2 = ". This means you will always make your decision after finding out about your group member’s contribution decisions. Your group member goes first and makes their own contribution decisions. And then, you see their decisions and make your own decision. At the end of each round, everyone will be informed about contributions to the group accounts and you will learn your earnings in that round. After reading information provided in these summary screens, do not forget to click next in a timely manner. This will prevent delays in the experiment."
        else:
            pt1="You and your group member will make contribution decisions simultaneously."
        return dict(
            self.player.TreatmentVars(),
            mover_title = mover_title,
            pt1=pt1,
            italics=italics,
            bold=bold,
            pt2=pt2,
            )
    def is_displayed(self):
        return not self.player.TreatmentVars()['simultaneous']

class Warning(Page):
    def vars_for_template(self):
        d=self.player.TreatmentVars()
        #predeclare the variables we'll use for the dict so their scope isn't limited to the if statements
        mover_title = ""
        pt1 = ""
        italics = ""
        bold = ""
        pt2 = ""
        if not d['simultaneous']:
            pt1 = "You are the "
            if self.player.id_in_group%2 == 1:
                self.player.participant.vars["id"]=1
                mover_title = "You Have Been Randomly Selected to be the First Mover"
                italics = "first mover"
                pt2 = ". This means you will always make your decision first. And then, you group member will observe your decisions and make their own decision. At the end of each round, you will be provided a round summary screen where we provide information about contributions to the group accounts and your earnings in that round. After reading information provided in these summary screens, do not forget to click next in a timely manner. This will prevent delays in the experiment."
            elif self.player.id_in_group%2 == 0:
                self.player.participant.vars["id"]=2
                mover_title = "You are Randomly Selected to be the Second Mover"
                italics = "second mover"
                pt2 = ". This means you will always make your decision after finding out about your group member’s contribution decisions. Your group member goes first and makes their own contribution decisions. And then, you see their decisions and make your own decision. At the end of each round, everyone will be informed about contributions to the group accounts and you will learn your earnings in that round. After reading information provided in these summary screens, do not forget to click next in a timely manner. This will prevent delays in the experiment."
        else:
            pt1="You and your group member will make contribution decisions simultaneously."
        return dict(
            self.player.TreatmentVars(),
            mover_title = mover_title,
            pt1=pt1,
            italics=italics,
            bold=bold,
            pt2=pt2,
            )
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
    #Message,
    #Warning,
    #Wait
]