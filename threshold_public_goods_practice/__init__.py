import random

from custom_templates.custom_funcs import *
from otree import common
from otree.api import *


author = 'Your name here'
doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'mtpgg_practice'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # we don't have to worry about a maximum value here because
    # the page will error if the total is too high and if we
    # try to base each max off of the base_tokens - the contribution
    # to the other group then that max value is only updated when
    # a submission attempt is made on the form, which leaves you able
    # to softlock yourself out of certain contribution combinations.
    pr_contribution_acc_a = models.IntegerField(min=0, initial=0, label="Your Contribution")
    pr_contribution_acc_b = models.IntegerField(min=0, initial=0, label="Your Contribution")
    # internal fields
    pr_acc_a_total = models.IntegerField(label="")
    pr_acc_b_total = models.IntegerField(label="")
    pr_thresh_a_met = models.BooleanField(label="")
    pr_thresh_b_met = models.BooleanField(label="")


# FUNCTIONS
# PAGES
class Practice(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(all_vars=player.participant.vars)


class PracticeGame(Page):
    # def get_timeout_seconds(self):
    #     return self.session.config['decision_timer']
    form_model = 'player'
    form_fields = ['pr_contribution_acc_a', 'pr_contribution_acc_b']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant_vars_dump(player)

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            player.TreatmentVars(),
            roundNum=player.round_number,
            all_vars=player.participant.vars,
            id_in_group=player.participant.vars.get("id", None),
        )

    @staticmethod
    def error_message(player: Player, values):  # entry checking
        d = player.TreatmentVars()
        if values['pr_contribution_acc_a'] < 0 or values['pr_contribution_acc_b'] < 0:
            return 'You cannot contribute negative tokens.'
        if values['pr_contribution_acc_a'] + values['pr_contribution_acc_b'] > d['base_tokens']:
            return 'You cannot contribute more tokens than you have.'


# Use what we've coded so far for the game as a parent class and create childclasses for it.
class p1Game(PracticeGame):
    template_name = 'threshold_public_goods_practice/Game.html'

    def vars_for_template(self):
        return dict(
            super().vars_for_template(),
            group_a_con="",
            group_b_con="",
            display_contributions=0,
        )

    def is_displayed(self):
        return not self.session.config['simultaneous'] and self.player.participant.vars["id"] == 1


class p2Game(PracticeGame):
    template_name = 'threshold_public_goods_practice/Game.html'

    def vars_for_template(self):
        d = self.player.TreatmentVars()
        group_a_con = random.choice(range(0, d['base_tokens'] + 1, d['increment']))
        group_b_con = random.choice(range(0, d['base_tokens'] + 1 - group_a_con, d['increment']))
        # prevent reloading the page from randomizing the contribution again
        self.participant.vars['practiceA'] = self.participant.vars.get('practiceA', group_a_con)
        self.participant.vars['practiceB'] = self.participant.vars.get('practiceB', group_b_con)
        return dict(
            super().vars_for_template(),
            group_a_con=self.participant.vars['practiceA'],
            group_b_con=self.participant.vars['practiceB'],
            display_contributions=1,
        )

    def is_displayed(self):
        return not self.session.config['simultaneous'] and self.player.participant.vars["id"] == 2


class p2plusGame(PracticeGame):
    template_name = 'threshold_public_goods_practice/Game.html'

    def vars_for_template(self):
        d = self.player.TreatmentVars()
        group_a_con = random.choice(
            range(
                0, d['base_tokens'] * (self.player.participant.vars["id"] - 1) + 1, d['increment']
            )
        )
        group_b_con = random.choice(
            range(
                0,
                d['base_tokens'] * (self.player.participant.vars["id"] - 1) + 1 - int(group_a_con),
                d['increment'],
            )
        )
        # prevent reloading the page from randomizing the contribution again
        self.participant.vars['practiceA'] = self.participant.vars.get('practiceA', group_a_con)
        self.participant.vars['practiceB'] = self.participant.vars.get('practiceB', group_b_con)
        return dict(
            super().vars_for_template(),
            group_a_con=self.participant.vars['practiceA'],
            group_b_con=self.participant.vars['practiceB'],
            display_contributions=1,
        )

    def is_displayed(self):
        return not self.session.config['simultaneous'] and self.player.participant.vars["id"] > 2


class SimGame(PracticeGame):  # simultaneous
    template_name = 'threshold_public_goods_practice/Game.html'

    def vars_for_template(self):
        return dict(
            super().vars_for_template(),
            all_vars=self.participant.vars,
            group_a_con="",
            group_b_con="",
            display_contributions=0,
        )

    def is_displayed(self):
        return self.session.config['simultaneous']


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        d = player.TreatmentVars()
        # Simulate the total contributions
        # make sure that these participant vars are initialized if they're not
        randA = random.choice(
            range(0, d['base_tokens'] * (d['group_size'] - 1) + 1, d['increment'])
        )
        randB = random.choice(
            range(0, d['base_tokens'] * (d['group_size'] - 1) + 1 - int(randA), d['increment'])
        )
        # prevent reloading the page from randomizing the contribution again
        player.participant.vars['practiceA'] = player.participant.vars.get('practiceA', randA)
        player.participant.vars['practiceB'] = player.participant.vars.get('practiceB', randB)
        player.participant.vars['vars_json_dump'][
            'PracticeGame-computer_con_A'
        ] = player.participant.vars.get('practiceA', randA)
        player.participant.vars['vars_json_dump'][
            'PracticeGame-computer_con_B'
        ] = player.participant.vars.get('practiceB', randB)
        # set up the proper group contributions
        groupConA = player.participant.vars['practiceA'] + player.pr_contribution_acc_a
        groupConB = player.participant.vars['practiceB'] + player.pr_contribution_acc_b
        # calculate the amount of tokens the player has left over
        kept = d['base_tokens'] - player.pr_contribution_acc_a - player.pr_contribution_acc_b
        # set up the return vars
        player.pr_acc_a_total = int(groupConA)
        player.pr_thresh_a_met = bool(groupConA >= d['threshold_high'])
        player.pr_acc_b_total = int(groupConB)
        player.pr_thresh_b_met = bool(groupConB >= d['threshold_low'])
        lostHigh = 0 if groupConA >= d['threshold_high'] else 1
        AEarn = d['value_high'] if player.pr_thresh_a_met else 0
        lostLow = 0 if groupConB >= d['threshold_low'] else 1
        BEarn = d['value_low'] if player.pr_thresh_b_met else 0
        # save the payoff to the datasheet otherwise it's lost to the void
        player.payoff = kept + AEarn + BEarn
        return dict(
            d,
            all_vars=player.participant.vars,
            roundNum=player.round_number,
            lostHigh=lostHigh,
            lostLow=lostLow,
            groupConA=groupConA - player.pr_contribution_acc_a,
            groupConB=groupConB - player.pr_contribution_acc_b,
            totConA=groupConA,
            totConB=groupConB,
            kept=kept,
            AEarn=AEarn,
            BEarn=BEarn,
            TotEarn=kept + AEarn + BEarn,
        )


class Start(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(player.TreatmentVars(), all_vars=player.participant.vars)


page_sequence = [Practice, p1Game, p2Game, p2plusGame, SimGame, Results, Start]
