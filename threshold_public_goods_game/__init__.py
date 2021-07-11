from custom_templates.custom_funcs import *
from otree import common
from otree.api import *


author = 'Your name here'
doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'mtpgg'
    players_per_group = None
    num_rounds = 15


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    timed_out_round = models.IntegerField()
    # we don't have to worry about a maximum value here because
    # the page will error if the total is too high and if we
    # try to base each max off of the base_tokens - the contribution
    # to the other group then that max value is only updated when
    # a submission attempt is made on the form, which leaves you able
    # to softlock yourself out of certain contribution combinations.
    contribution_acc_a = models.IntegerField(min=0, initial=0, label="Your Contribution")
    contribution_acc_b = models.IntegerField(min=0, initial=0, label="Your Contribution")
    # internal fields
    acc_a_total = models.IntegerField(label="")
    acc_b_total = models.IntegerField(label="")
    thresh_a_met = models.BooleanField(label="")
    thresh_b_met = models.BooleanField(label="")


# FUNCTIONS
def after_arrive(subsession: Subsession):
    mixedPlayers = subsession.get_players()  # mix of both active and inactive player objects
    d = mixedPlayers[0].TreatmentVars()
    matrix = (
        []
    )  # fill up a matrix in numerical id order (note, we don't use self.get_matrix here because we want to control group size)
    players = []
    timed_out = []  # separate matrix for players that timed out
    for n in range(d['group_size']):  # create the matrix for zipping
        players.append([])
        timed_out.append([])
    # init indexes for sim game sort
    pl_y = 0
    to_y = 0
    for pl in mixedPlayers:
        if not d['simultaneous']:  # if you have to worry about maintaining id in group
            if (
                pl.participant.vars.get('timed_out_round', 0) == 0
                and not pl.participant.vars.get('groupmate_timed_out', None) == True
            ):
                players[(pl.id_in_group - 1) % d['group_size']].append(pl)
            else:
                timed_out[(pl.id_in_group - 1) % d['group_size']].append(pl)
        else:  # otherwise make sure the groups are evenly filled by the given players
            if (
                pl.participant.vars.get('timed_out_round', 0) == 0
                and not pl.participant.vars.get('groupmate_timed_out', None) == True
            ):
                players[pl_y].append(pl)
                pl_y = (pl_y + 1) % d['group_size']
            else:
                timed_out[to_y].append(pl)
                to_y = (to_y + 1) % d['group_size']
    # add the players who are still in to the matrix
    matrix = [list(x) for x in zip(*players)]
    # shuffle the matrix
    finalMatrix = common._group_randomly(matrix, fixed_id_in_group=not d['simultaneous'])
    # add the players who aren't still in in their own separate groups
    finalMatrix = finalMatrix + [list(x) for x in zip(*timed_out)]
    subsession.set_group_matrix(finalMatrix)


def group_by_arrival_time_method(subsession: Subsession, waiting_players):
    import random

    d = (subsession.get_players()[0]).TreatmentVars()
    participants = [
        pl.participant for pl in subsession.get_players()
    ]  # There is no get_participants function for subsession objects
    # a few debug prints
    # print("number of waiting players: "+str(len(waiting_players)))
    # print("lower limit: "+str(d['waiting_room_lowerlimit']))
    # handles the case where the number of players is less than the lower limit but
    # there are no more players left to wait
    # important to note that this wait page is the first thing that happens in the round -
    # so anyone where round_number is < the waiting players is before them and anyone whose
    # round number is >= the waiting players is after them
    special_case = True
    for partic in participants:
        # if someone hasn't gotten here yet, break because that invalidates the criteria
        if partic._index_in_pages < waiting_players[0].participant._index_in_pages:
            special_case = False
            break
    # if you broke there
    if special_case:
        if len(waiting_players) >= d['group_size']:
            return random.sample(waiting_players, d['group_size'])
    # handles the normal case
    if (
        len(waiting_players) >= d['waiting_room_lowerlimit']
        and len(waiting_players) >= d['group_size']
    ):
        # if you've got enough people get a random sample of them and put that into a group
        return random.sample(waiting_players, d['group_size'])


# PAGES
class GroupWaitAsyncGame(WaitPage):
    # Important note: Wait pages do not like to be templated and will, in fact, throw a fit if you try to do "template_name = " on them
    group_by_arrival_time = True  # this triggers the group_by_arrival_time_method in the subsection class under models.py
    title_text = "Please wait while we form your group. This should not take long."
    body_text = "Please do not leave this page.\n\nOnce your group is constructed, the experiment will start immediately.\n\nIf you do not put your answers in a timely manner, you will be removed from the study."

    @staticmethod
    def is_displayed(player: Player):
        return not player.session.config['synchronous_game']


class GroupWaitSyncGame(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = 'after_arrive'
    title_text = "Please wait while we form your group. This should not take long."
    body_text = "Please do not leave this page.\n\nOnce your group is constructed, the experiment will start immediately.\n\nIf you do not put your answers in a timely manner, you will be removed from the study."

    @staticmethod
    def is_displayed(player: Player):
        return player.session.config['synchronous_game']


class Game(Page):
    @staticmethod
    def get_timeout_seconds(player: Player):
        return player.session.config['decision_timer']

    form_model = 'player'
    form_fields = ['contribution_acc_a', 'contribution_acc_b']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        d = player.TreatmentVars()
        player.participant.vars['timed_out_round'] = 0
        player.timed_out_round = player.participant.vars['timed_out_round']
        import random

        # if you time out do the bot logic
        if timeout_happened:
            # pick your first contribution
            # if base_tokens = 20 and increment = 10 then the range function will return 0, 10, 20
            # and random will chose between them
            A = random.choice(range(0, d['base_tokens'] + 1, d['increment']))
            # same basic principle as above but you have less tokens to work with
            B = random.choice(range(0, d['base_tokens'] + 1 - A, d['increment']))
            # set the player response values
            player.contribution_acc_a = A
            player.contribution_acc_b = B
            player.participant.vars['timed_out'] = True
            player.timed_out_round = player.round_number
            others = player.get_others_in_group()
            for pl in others:
                pl.participant.vars['groupmate_timed_out'] = True
        player.participant_vars_dump(player)

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            player.TreatmentVars(),
            all_vars=player.participant.vars,
            roundNum=player.round_number,
            id_in_group=player.id_in_group,
        )

    @staticmethod
    def error_message(player: Player, values):  # entry checking
        d = player.TreatmentVars()
        if values['contribution_acc_a'] < 0 or values['contribution_acc_b'] < 0:
            return 'You cannot contribute negative tokens.'
        if values['contribution_acc_a'] + values['contribution_acc_b'] > d['base_tokens']:
            return 'You cannot contribute more tokens than you have.'


# Use what we've coded so far for the game as a parent class and create childclasses for it.
# note: this is probably less resource efficient than creating multiple apps.
class p1Game(Game):
    template_name = 'threshold_public_goods_game/Game.html'

    def vars_for_template(self):
        return dict(
            super().vars_for_template(),
            group_a_con="",
            group_b_con="",
            display_contributions=0,
        )

    def is_displayed(self):
        return not self.session.config['simultaneous'] and self.player.id_in_group == 1


class p2Game(Game):
    template_name = 'threshold_public_goods_game/Game.html'

    def vars_for_template(self):
        players = self.player.group.get_players()
        group_a_con = 0
        group_b_con = 0
        for pl in players:
            if not pl == self.player:  # this isn't the point for your contribution to show up
                group_a_con += pl.contribution_acc_a
                group_b_con += pl.contribution_acc_b
        return dict(
            super().vars_for_template(),
            group_a_con=group_a_con,
            group_b_con=group_b_con,
            display_contributions=1,
        )

    def is_displayed(self):
        return not self.session.config['simultaneous'] and self.player.id_in_group == 2


class p3Game(Game):
    template_name = 'threshold_public_goods_game/Game.html'

    def vars_for_template(self):
        players = self.player.group.get_players()
        group_a_con = 0
        group_b_con = 0
        for pl in players:
            if not pl == self.player:  # this isn't the point for your contribution to show up
                group_a_con += pl.contribution_acc_a
                group_b_con += pl.contribution_acc_b
        return dict(
            super().vars_for_template(),
            group_a_con=group_a_con,
            group_b_con=group_b_con,
            display_contributions=1,
        )

    def is_displayed(self):
        return not self.session.config['simultaneous'] and self.player.id_in_group == 3


class SeqWait(WaitPage):
    template_name = "threshold_public_goods_game/CustWaitPage.html"

    @staticmethod
    def vars_for_template(player: Player):
        if player.session.config['group_size'] == 2:
            if player.id_in_group == 1:
                return dict(
                    title="Please Wait.",
                    text="Please wait for the second mover to make their contribution decision.",
                )
            else:
                return dict(
                    title="Please Wait.",
                    text="Please wait for the first mover to make their contribution decision. Once they are done, you will see their contribution decision. Then, you will be asked to make your own contribution decision.",
                )
        else:
            if player.id_in_group == 1:
                return dict(
                    title="Please Wait.",
                    text="Please wait for the second mover to make their contribution decision.",
                )
            elif player.id_in_group == 2:
                return dict(
                    title="Please Wait.",
                    text="Please wait for the first mover to make their contribution decision. Once they are done, you will see their contribution decision. Then, you will be asked to make your own contribution decision.",
                )
            else:  # player 3+
                return dict(
                    title="Please Wait.",
                    text="Please wait for the first and the second movers to make their contribution decisions.",
                )

    @staticmethod
    def is_displayed(player: Player):
        return not player.session.config['simultaneous']


class SeqWait2(WaitPage):
    template_name = "threshold_public_goods_game/CustWaitPage.html"

    @staticmethod
    def vars_for_template(player: Player):
        if player.id_in_group == 3:  # shown just to player 3
            return dict(
                title="Please Wait.",
                text="Please wait for the second mover to make their contribution decision. Once they are done, you will see their contribution decision. Then, you will be asked to make your own contribution decision.",
            )
        else:
            return dict(
                title="Please Wait.",
                text="Please wait for the third mover to make their contribution decision.",
            )

    @staticmethod
    def is_displayed(player: Player):
        return (not player.session.config['simultaneous']) and player.session.config[
            'group_size'
        ] == 3


class SimGame(Game):  # simultaneous
    template_name = 'threshold_public_goods_game/Game.html'

    def vars_for_template(self):
        return dict(
            super().vars_for_template(),
            group_a_con="",
            group_b_con="",
            display_contributions=0,
        )

    def is_displayed(self):
        return self.session.config['simultaneous']


class ResWait(WaitPage):
    title_text = "Please wait until everyone finishes. This should not take long."
    body_text = "Please do not leave this page."

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        if (
            player.participant.vars.get('timed_out', None) == True
        ):  # if you've timed out, go to the timeout app and stop being here.
            player.participant.vars['timed_out_round'] = player.round_number
            return upcoming_apps[-1]


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        d = player.TreatmentVars()
        # handle dropping groupmates
        dropped = 0
        if player.participant.vars.get('groupmate_timed_out', None) == True:
            dropped = 1
        # Calculate the total contributions for each group
        players = player.group.get_players()
        groupConA = 0
        groupConB = 0
        for pl in players:
            groupConA += pl.contribution_acc_a
            groupConB += pl.contribution_acc_b
        # calculate the amount of tokens the player has left over
        kept = d['base_tokens'] - player.contribution_acc_a - player.contribution_acc_b
        # set up the return vars
        for pl in players:
            pl.acc_a_total = int(groupConA)
            pl.thresh_a_met = bool(groupConA >= d['threshold_high'])
            pl.acc_b_total = int(groupConB)
            pl.thresh_b_met = bool(groupConB >= d['threshold_low'])
        lostHigh = 0 if groupConA >= d['threshold_high'] else 1
        AEarn = d['value_high'] if player.thresh_a_met else 0
        lostLow = 0 if groupConB >= d['threshold_low'] else 1
        BEarn = d['value_low'] if player.thresh_b_met else 0
        # save the payoff to the datasheet otherwise it's lost to the void
        player.payoff = kept + AEarn + BEarn
        # save to participant vars
        player.participant.vars['vars_json_dump'][
            'Game-id_in_group-' + str(player.round_number)
        ] = player.id_in_group
        player.participant.vars['vars_json_dump'][
            'Game-_id_in_subsesion-' + str(player.round_number)
        ] = player.group.id_in_subsession
        player.participant.vars['vars_json_dump'][
            'Game-acc_a_total-' + str(player.round_number)
        ] = int(player.acc_a_total)
        player.participant.vars['vars_json_dump'][
            'Game-acc_b_total-' + str(player.round_number)
        ] = int(player.acc_b_total)
        player.participant.vars['vars_json_dump'][
            'Game-thresh_a_met-' + str(player.round_number)
        ] = player.thresh_a_met
        player.participant.vars['vars_json_dump'][
            'Game-thresh_b_met-' + str(player.round_number)
        ] = player.thresh_b_met
        player.participant.vars['vars_json_dump']['Game-payoff-' + str(player.round_number)] = int(
            player.payoff
        )
        return dict(
            d,
            all_vars=player.participant.vars,
            dropped=dropped,
            roundNum=player.round_number,
            lostHigh=lostHigh,
            lostLow=lostLow,
            groupConA=groupConA - player.contribution_acc_a,
            groupConB=groupConB - player.contribution_acc_b,
            totConA=groupConA,
            totConB=groupConB,
            kept=kept,
            AEarn=AEarn,
            BEarn=BEarn,
            TotEarn=kept + AEarn + BEarn,
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # If it's the last round save the data to the participant otherwise
        # we won't be able to access it in the next app
        if player.round_number == player.TreatmentVars()['total_rounds']:
            player.participant.vars['GameRounds'] = [pl.payoff for pl in player.in_all_rounds()]
            player.participant.vars['a_total'] = [pl.acc_a_total for pl in player.in_all_rounds()]
            player.participant.vars['b_total'] = [pl.acc_b_total for pl in player.in_all_rounds()]

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        if (
            player.participant.vars.get('groupmate_timed_out', None) == True
            or player.round_number == player.TreatmentVars()['total_rounds']
        ):
            return upcoming_apps[0]


page_sequence = [
    GroupWaitAsyncGame,
    GroupWaitSyncGame,
    p1Game,
    SeqWait,
    p2Game,
    SeqWait,
    p3Game,
    SimGame,
    ResWait,
    Results,
]
