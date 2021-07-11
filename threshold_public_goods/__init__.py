from custom_templates.custom_funcs import *
from otree.api import *


author = 'Your name here'
doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'mtpg'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # attention check and intro
    p_ID = models.StringField(label='Paste your Prolific ID here')
    consent = models.BooleanField(initial=False, label='')
    attention_check_1 = models.IntegerField(
        label="This question is to check your attention. Please select rabbit",
        initial=0,
        choices=[[0, 'no selection'], [0, 'dog'], [0, 'cat'], [1, 'rabbit']],
    )
    attention_check_2 = models.IntegerField(
        label="This question is to check your attention. Please select hello",
        initial=0,
        choices=[[0, 'no selection'], [0, 'bye'], [1, 'hello'], [0, 'good']],
    )
    # Questions Page (entirely hypothetical, not actual game data)
    oConA = models.IntegerField()  # other person's contribution to group A
    oConB = models.IntegerField()  # other person's contribution to group B
    yConA = models.IntegerField()  # your contribution to group A
    yConB = models.IntegerField()  # your contribution to group B
    yRem = models.IntegerField()  # your remaining tokens
    yPay = models.IntegerField()  # your total payout
    payOutB = models.IntegerField()  # your payout from group B
    # Note: Group A will never pay out, group B will always payout, and you will always have at least one remaining token.
    question1 = models.IntegerField(
        label="Is the threshold for Group Account A met?",
        initial=-1,
        choices=[[-1, "No Selection"], [1, "Yes"], [0, "No"]],
    )
    question2 = models.IntegerField(
        label="Is the threshold for Group Account B met?",
        initial=-1,
        choices=[[-1, "No Selection"], [1, "Yes"], [0, "No"]],
    )
    question3 = models.IntegerField(
        label="What are your total earnings in this hypothetical situation?"
    )


# FUNCTIONS
def question1_error_message(player: Player, value):
    if value == -1:
        return "Please make sure to answer all questions. You cannot move forward without answering all of the questions correctly"
    if value == 1:
        return 'Since the total tokens contributed to Group Account A is less than its threshold, the threshold is not met.'


def question2_error_message(player: Player, value):
    if value == -1:
        return "Please make sure to answer all questions. You cannot move forward without answering all of the questions correctly"
    if value == 0:
        return (
            'Since the total tokens contributed to Group Account B is more than or equal to its threshold, the threshold is met. Thus, you will receive '
            + str(player.payOutB)
            + ' tokens from this account'
        )


def question3_error_message(player: Player, value):
    if int(value) != player.yPay:
        sR = ""
        if player.yRem > 1:  # pluralize tokens if you've got multiple remaining
            sR = "s"
        return (
            "You have "
            + str(player.yRem)
            + " token"
            + str(sR)
            + " remaining from your endowment. You did not receive any tokens from Group Account A since the threshold was not met. You received "
            + str(player.payOutB)
            + " tokens from Group Account B since the threshold was met. Thus, your earnings in this game are "
            + str(player.yRem)
            + "+"
            + str(player.payOutB)
            + "="
            + str(player.yPay)
            + " tokens."
        )


# PAGES
class PID_Begin(Page):
    form_model = 'player'
    form_fields = ['p_ID']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.vars['p_id_begin'] = player.p_ID
        player.participant_vars_dump(player)

    @staticmethod
    def error_message(player: Player, values):
        if len(values['p_ID']) != 24:
            return 'You must enter a valid 24 character Prolific ID.'


class Informed_Consent(Page):
    form_model = 'player'
    form_fields = ['consent']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            player.TreatmentVars(),
            all_vars=player.participant.vars,
            informed_consent=player.session.config['consent'],
            consent_link=player.session.config['consent_link'],
        )

    @staticmethod
    def before_next_page(
        player: Player, timeout_happened
    ):  # set up participant vars we'll use later
        player.participant.vars['timed_out'] = False
        player.participant.vars['groupmate_timed_out'] = False
        player.participant_vars_dump(player)
        #player.participant.vars['vars_json_dump']['id_in_session'] = player.participant.id_in_session
        #player.participant.vars['vars_json_dump']['code'] = player.participant.code
        #player.participant.vars['vars_json_dump']['label'] = player.participant.label
        d = player.TreatmentVars()
        if not d['simultaneous']:  # record participant id
            player.participant.vars["id"] = player.id_in_group % d['group_size']


class Overview(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(player.TreatmentVars(), all_vars=player.participant.vars)


class Rules(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(player.TreatmentVars(), all_vars=player.participant.vars)


class GameOverview(Page):
    form_model = 'player'
    form_fields = ['attention_check_1']

    @staticmethod
    def vars_for_template(player: Player):
        d = player.TreatmentVars()
        return dict(
            d,
            all_vars=player.participant.vars,
            total_tokens=d['base_tokens'] * d['group_size'],
            other_part=d['group_size'] - 1,
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant_vars_dump(player)


class GameOverview2(Page):
    form_model = 'player'
    form_fields = ['attention_check_2']

    @staticmethod
    def vars_for_template(player: Player):
        d = player.TreatmentVars()
        return dict(
            d, all_vars=player.participant.vars, total_tokens=d['base_tokens'] * d['group_size']
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant_vars_dump(player)


class TotalEarnings(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(player.TreatmentVars(), all_vars=player.participant.vars)


class ContributionDecisions(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(player.TreatmentVars(), all_vars=player.participant.vars)


def tokenSFormat(con):  # format contribution as "token" if 1, "tokens" otherwise
    ret = "" + str(con)
    ret += " token"
    if not con == 1:
        ret += "s"
    return ret


class Question(Page):
    form_model = 'player'
    form_fields = ['question1', 'question2', 'question3']

    @staticmethod
    def vars_for_template(player: Player):
        d = player.TreatmentVars()
        player.oConA = 0  # other person's contribution to group A
        player.oConB = d[
            'base_tokens'
        ]  # other person's contribution to group B (always contributes all their tokens to B)
        player.yConB = d['threshold_low'] - player.oConB  # you contribute the bare minimum
        player.yConA = (
            d['base_tokens'] - player.yConB
        ) // 2  # your contribution to group A (give about half (integer division))
        player.yRem = d['base_tokens'] - player.yConB - player.yConA  # your remaining tokens
        player.payOutB = d['value_low']  # your payout from group B
        player.yPay = player.yRem + player.payOutB  # your total payout
        oConAt = tokenSFormat(player.oConA)
        oConBt = tokenSFormat(player.oConB)
        yConAt = tokenSFormat(player.yConA)
        yConBt = tokenSFormat(player.yConB)
        return dict(
            player.TreatmentVars(),
            all_vars=player.participant.vars,
            oConAt=oConAt,
            oConBt=oConBt,
            yConAt=yConAt,
            yConBt=yConBt,
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant_vars_dump(player)


class Message(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(player.TreatmentVars(), all_vars=player.participant.vars)


class Your_role(Page):
    @staticmethod
    def vars_for_template(player: Player):
        d = player.TreatmentVars()
        player.participant.vars["id"] = player.id_in_group % player.session.config['group_size']
        if player.participant.vars["id"] == 0:
            player.participant.vars["id"] = player.session.config['group_size']
        return dict(
            player.TreatmentVars(),
            all_vars=player.participant.vars,
            p_id=player.participant.vars["id"],
        )

    @staticmethod
    def is_displayed(player: Player):
        return not player.TreatmentVars()['simultaneous']


class Wait(WaitPage):
    title_text = "Please wait while we form your group. This should not take long."
    body_text = "Please do not leave this page.\n\nOnce your group is constructed, the experiment will start immediately.\n\nIf you do not put your answers in a timely manner, you will be removed from the study."

    @staticmethod
    def is_displayed(player: Player):
        return player.session.config['synchronous_game']


page_sequence = [
    # PID_Begin,
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
