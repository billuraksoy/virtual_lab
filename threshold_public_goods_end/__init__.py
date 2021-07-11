import json

from custom_templates.custom_funcs import *
from otree.api import *


author = 'Your name here'
doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'mtpge'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    birth_year = models.IntegerField(min=1900, max=2020, label="What is your year of birth?")
    gender = models.IntegerField(
        choices=[[0, 'Male'], [1, 'Female'], [2, 'Other']], label="What is your gender identity?"
    )
    # #removed question, kept here for potential future use
    # education = models.IntegerField(
    #     label="What is the highest education qualification you have attained?",
    #     choices=[
    #         [0,'Did not complete High School'],
    #         [1,'Graduated from High School'],
    #         [2,'Some College Degree'],
    #         [3,'Bachelor’s Degree'],
    #         [4,'Master’s Degree'],
    #         [5,'Ph.D. or higher']
    #     ]
    #     )
    income = models.IntegerField(
        label="Please select your household annual income from the options below:",
        choices=[
            [0, 'less than $20,000'],
            [1, '$20,000-$39,999'],
            [2, '$40,000-$59,999'],
            [3, '$60,000-$79,999'],
            [4, '$80,000-$99,999'],
            [5, '$100,000 or more'],
        ],
    )
    def make_field(label):
        return models.BooleanField(
            label=label,
            widget=widgets.CheckboxInput,
            initial=False,
            blank=True
            )
    Wh = make_field("White")
    Bl = make_field("Black or African American")
    Na = make_field("American Indian or Alaskan Native")
    As = make_field("Asian")
    Nh = make_field("Native Hawaiian or Pacific Islander")
    Hi = make_field("Hispanic or Latino")
    Me = make_field("Middle Eastern or Arab")
    OtherBool = make_field("Other (please state below)")
    other = models.StringField(blank=True, label="")
    risk = models.IntegerField(
        label='Please answer the following question using a 1–10 scale, where 1 = completely unwilling and 10 = completely willing: Rate your willingness to take risks in general.',
        choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        widget=widgets.RadioSelectHorizontal,
    )
    # #code used for student testing
    # major = models.StringField(label="Please enter your full name as it appears on Howdy to receive your bonus grade.")
    paypal = models.StringField(label="PayPal:", blank=True)
    venmo = models.StringField(label="Venmo Username:", blank=True)
    venmo_number = models.StringField(label="Venmo Phone Number:", blank=True)
    strategy = models.LongStringField(
        label="Did you use a particular strategy when making your decisions in Part 1 and/or Part 2?"
    )
    # #removed/changed questions
    # understanding = models.LongStringField(label="Were the instructions easy to understand?")
    # thoughts = models.LongStringField(label="What did you think about the experiment?")
    # suggestions = models.LongStringField(label="Do you have any suggestions for us to improve the study?")
    anything_else = models.LongStringField(
        label="Is there anything else you would like to share with us?"
    )
    new_understanding = models.IntegerField(
        label="To what extent do you agree with the following statement: \"The instructions were easy to understand\"",
        choices=[
            [0, 'Strongly Agree'],
            [1, 'Agree'],
            [2, 'Undecided'],
            [3, 'Disagree'],
            [4, 'Strongly Disagree'],
        ],
    )
    # internal fields
    round_chosen_for_payment_P1 = models.IntegerField(label="")
    groupAThresholdMet = models.BooleanField(label="")
    groupBThresholdMet = models.BooleanField(label="")
    groupATotalContribution = models.IntegerField(label="")
    groupBTotalContribution = models.IntegerField(label="")
    participant_vars = models.LongStringField()
    round_chosen_for_payment_P2 = models.IntegerField(label="")
    Part2Earnings = models.FloatField(label="")


# FUNCTIONS
def make_field(label):
    return models.BooleanField(label=label, widget=widgets.CheckboxInput, initial=False, blank=True)


def other_error_message(player: Player, value):
    if player.OtherBool and value == None:
        return 'If you select Other, you must specify in the provided field.'


# PAGES
class ThankYou(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(all_vars=player.participant.vars)


class Survey(Page):
    form_model = 'player'
    form_fields = [
        'birth_year',
        'gender',
        'income',
        'Wh',
        'Bl',
        'Na',
        'As',
        'Nh',
        'Hi',
        'Me',
        'OtherBool',
        'other',
        'risk',
    ]

    @staticmethod
    def error_message(player: Player, values):
        lst = ['Wh', 'Bl', 'Na', 'As', 'Nh', 'Hi', 'Me', 'OtherBool']
        error = True
        for i in lst:
            error = error and not values[i]
        if error:
            return "You must select at least one ethnicity."

    @staticmethod
    def vars_for_template(player: Player):
        return dict(all_vars=player.participant.vars)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant_vars_dump(player)


class Paypal(Page):
    form_model = 'player'
    form_fields = ['paypal', 'venmo', 'venmo_number']

    @staticmethod
    def error_message(player: Player, values):
        if values['paypal'] == None and (values['venmo'] == None or values['venmo_number'] == None):
            return "You must enter identifying information for either a PayPal or a Venmo account."

    @staticmethod
    def vars_for_template(player: Player):
        return dict(all_vars=player.participant.vars)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant_vars_dump(player)


class Survey2(Page):
    form_model = 'player'
    form_fields = ['new_understanding', 'strategy', 'anything_else']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(all_vars=player.participant.vars)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant_vars_dump(player)


class Summary(Page):
    @staticmethod
    def vars_for_template(player: Player):
        import random

        d = player.TreatmentVars()
        # seed the rng based on a value that will remain the same on refresh
        PayingRoundP1 = ""
        TokensEarnedP1 = ""
        PayingRoundP2 = ""
        TokensEarnedP2 = ""
        TokensKeptP2 = 0
        ME1 = 0
        ME2 = 0
        if player.participant.vars.get('groupmate_timed_out', None) == True:
            PayingRoundP1 = "Because your partner disconnected and since we need an even number of subjects for this study, you have been removed from Part 1. But you will still earn 10 tokens from Part 1."
            TokensEarnedP1 = "10"
            ME1 = 10
        else:
            random.seed(player.birth_year * (1 + player.gender) * (1 + player.income))
            num_paying_rounds = 1
            rounds = player.participant.vars['GameRounds']
            a_totals = player.participant.vars['a_total']
            b_totals = player.participant.vars['b_total']
            # print(rounds)
            if (
                num_paying_rounds > 1
            ):  # as coded this only pays out multiple rounds for the first part
                TokensEarnedP1 = "Rounds chosen for payment:"
                TokensEarnedP1 = "in these rounds: "
                payRounds = random.sample(range(0, d['total_rounds']), num_paying_rounds)
                ME1 = 0
                for pRound in payRounds:
                    ME1 += rounds[pRound]
                    PayingRoundP1 += " " + str(pRound + 1)
                    TokensEarnedP1 += " " + str(rounds[pRound])
                    player.round_chosen_for_payment_P1 = pRound
            else:
                PayingRoundP1 = "Round chosen for payment: "
                TokensEarnedP1 = "in this round: "
                payRound1 = random.choice(range(0, d['total_rounds']))
                PayingRoundP1 += str(payRound1 + 1)
                TokensEarnedP1 += str(int(rounds[payRound1]))
                ME1 = rounds[payRound1]
                player.round_chosen_for_payment_P1 = payRound1 + 1
                player.groupAThresholdMet = a_totals[payRound1] >= d['threshold_high']
                player.groupBThresholdMet = b_totals[payRound1] >= d['threshold_low']
                player.groupATotalContribution = a_totals[payRound1]
                player.groupBTotalContribution = b_totals[payRound1]
        # Part2
        PayingRoundP2 = str(player.participant.vars['keptR'])
        # The round where you recieve is stored here and may be diff to the round you kept: pl.participant.vars['recR']
        TokensKeptP2 = str(player.participant.vars['kept'])
        TokensEarnedP2 = str(player.participant.vars['rec'])
        player.round_chosen_for_payment_P2 = player.participant.vars['keptR']
        ME2 = float(TokensKeptP2) * 0.30 + float(TokensEarnedP2) * 0.30
        player.Part2Earnings = ME2
        player.payoff = (
            float(ME1) + float(ME2) + float(player.session.config['participation_payment'])
        )
        # JSON Append
        player.participant.vars['vars_json_dump']['Part1Earnings'] = float(ME1)
        player.participant.vars['vars_json_dump']['Part2Earnings'] = float(ME2)
        player.participant.vars['vars_json_dump']['TotalEarnings'] = float(player.payoff)
        player.participant_vars = json.dumps(player.participant.vars['vars_json_dump'])
        return dict(
            d,
            all_vars=player.participant.vars,
            PayingRoundP1=PayingRoundP1,
            PayingRoundP2=PayingRoundP2,
            TokensEarnedP1=TokensEarnedP1,
            TokensEarnedP2=TokensEarnedP2,
            TokensKeptP2=TokensKeptP2,
            Part1Earnings=ME1,
            Part2Earnings=ME2,
            TotalEarnings=player.payoff,
        )


page_sequence = [ThankYou, Survey, Paypal, Survey2, Summary]
