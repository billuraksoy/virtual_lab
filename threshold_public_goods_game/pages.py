from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class GroupWaitAsyncGame(WaitPage):
    #Important note: Wait pages do not like to be templated and will, in fact, throw a fit if you try to do "template_name = " on them
    group_by_arrival_time=True #this triggers the group_by_arrival_time_method in the subsection class under models.py
    title_text="Please wait while we form your group. This should not take long."
    body_text="Please do not leave this page.\n\nOnce your group is constructed, the experiment will start immediately.\n\nIf you do not put your answers in a timely manner, you will be removed from the study."
    def is_displayed(self):
        return not self.session.config['synchronous_game']
class GroupWaitSyncGame(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = 'after_arrive'
    title_text="Please wait while we form your group. This should not take long."
    body_text="Please do not leave this page.\n\nOnce your group is constructed, the experiment will start immediately.\n\nIf you do not put your answers in a timely manner, you will be removed from the study."
    def is_displayed(self):
        return self.session.config['synchronous_game']
class Game(Page):
    def get_timeout_seconds(self):
        return self.session.config['decision_timer']
    form_model = 'player'
    form_fields = ['contribution_acc_a','contribution_acc_b']

    def before_next_page(self):
        d=self.player.TreatmentVars()
        self.participant.vars['timed_out_round']=0
        self.player.timed_out_round=self.participant.vars['timed_out_round']
        import random
        # if you time out do the bot logic
        if self.timeout_happened:
            # pick your first contribution
            # if base_tokens = 20 and increment = 10 then the range function will return 0, 10, 20 
            # and random will chose between them
            A = random.choice(range(0,d['base_tokens']+1,d['increment']))
            # same basic principle as above but you have less tokens to work with
            B = random.choice(range(0,d['base_tokens']+1-A,d['increment']))
            # set the player response values
            self.player.contribution_acc_a = A
            self.player.contribution_acc_b = B
            self.participant.vars['timed_out']=True
            self.player.timed_out_round=self.player.round_number
            others = self.player.get_others_in_group()
            for pl in others:
                pl.participant.vars['groupmate_timed_out']=True
        self.player.participant_vars_dump(self)

    def vars_for_template(self):
        return dict( 
            self.player.TreatmentVars(),
            all_vars = self.participant.vars,
            roundNum = self.round_number,
            id_in_group = self.player.id_in_group
            )

    def error_message(self, values): # entry checking
        d=self.player.TreatmentVars()
        if values['contribution_acc_a'] < 0 or values['contribution_acc_b'] < 0:
            return 'You cannot contribute negative tokens.'
        if values['contribution_acc_a'] + values['contribution_acc_b'] > d['base_tokens']:
            return 'You cannot contribute more tokens than you have.'

#Use what we've coded so far for the game as a parent class and create childclasses for it.
class p1Game(Game):
    template_name = 'threshold_public_goods_game/Game.html'
    def vars_for_template(self):
        return dict(
            super().vars_for_template(),
            group_a_con="",
            group_b_con="",
            display_contributions = 0,
            )
    def is_displayed(self):
        return not self.session.config['simultaneous'] and self.player.id_in_group==1

class p2Game(Game):
    template_name = 'threshold_public_goods_game/Game.html'
    def vars_for_template(self):
        players = self.player.group.get_players()
        group_a_con = 0
        group_b_con = 0
        for pl in players:
            if not pl==self.player:#this isn't the point for your contribution to show up
                group_a_con += pl.contribution_acc_a
                group_b_con += pl.contribution_acc_b

        return dict(
            super().vars_for_template(),
            group_a_con=group_a_con,
            group_b_con=group_b_con,
            display_contributions = 1,
            )
    def is_displayed(self):
        return not self.session.config['simultaneous'] and self.player.id_in_group==2

class p3Game(Game):
    template_name = 'threshold_public_goods_game/Game.html'
    def vars_for_template(self):
        players = self.player.group.get_players()
        group_a_con = 0
        group_b_con = 0
        for pl in players:
            if not pl==self.player:#this isn't the point for your contribution to show up
                group_a_con += pl.contribution_acc_a
                group_b_con += pl.contribution_acc_b

        return dict(
            super().vars_for_template(),
            group_a_con=group_a_con,
            group_b_con=group_b_con,
            display_contributions = 1,
            )
    def is_displayed(self):
        return not self.session.config['simultaneous'] and self.player.id_in_group==3

class SeqWait(WaitPage):
    template_name="threshold_public_goods_game/CustWaitPage.html"
    def vars_for_template(self):
        if self.session.config['group_size']==2:
            if self.player.id_in_group==1:
                return dict(title="Please Wait.",text="Please wait for the second mover to make their contribution decision.")
            else:
                return dict(title="Please Wait.",text="Please wait for the first mover to make their contribution decision. Once they are done, you will see their contribution decision. Then, you will be asked to make your own contribution decision.")
        else:
            if self.player.id_in_group ==1:
                return dict(title="Please Wait.",text="Please wait for the second mover to make their contribution decision.")
            elif self.player.id_in_group==2:
                return dict(title="Please Wait.",text="Please wait for the first mover to make their contribution decision. Once they are done, you will see their contribution decision. Then, you will be asked to make your own contribution decision.")
            else:#player 3+
                return dict(title="Please Wait.",text="Please wait for the first and the second movers to make their contribution decisions.")
    def is_displayed(self):
        return not self.session.config['simultaneous']

class SeqWait2(WaitPage):
    template_name="threshold_public_goods_game/CustWaitPage.html"
    def vars_for_template(self):
        if self.player.id_in_group==3:#shown just to player 3
            return dict(title="Please Wait.",text="Please wait for the second mover to make their contribution decision. Once they are done, you will see their contribution decision. Then, you will be asked to make your own contribution decision.")
        else:
            return dict(title="Please Wait.",text="Please wait for the third mover to make their contribution decision.")
    def is_displayed(self):
        return (not self.session.config['simultaneous']) and self.session.config['group_size']==3

class SimGame(Game):#simultaneous
    template_name = 'threshold_public_goods_game/Game.html'
    def vars_for_template(self):
        return dict(
            super().vars_for_template(),
            group_a_con="",
            group_b_con="",
            display_contributions = 0,
            )
    def is_displayed(self):
        return self.session.config['simultaneous']

class ResWait(WaitPage):
    title_text = "Please wait until everyone finishes. This should not take long."
    body_text = "Please do not leave this page."
    def app_after_this_page(self, upcoming_apps):
        if self.participant.vars.get('timed_out', None)==True: # if you've timed out, go to the timeout app and stop being here.
            self.participant.vars['timed_out_round']=self.round_number
            return upcoming_apps[-1]

class Results(Page):
    def vars_for_template(self):
        d=self.player.TreatmentVars()
        #handle dropping groupmates
        dropped = 0
        if self.participant.vars.get('groupmate_timed_out', None)==True:
            dropped=1
                
        # Calculate the total contributions for each group
        players = self.player.group.get_players()
        groupConA = 0
        groupConB = 0
        for pl in players:
            groupConA += pl.contribution_acc_a
            groupConB += pl.contribution_acc_b
        
        # # Hardcoded text strings Aw=A win, Bl = B loss, etc.
        # Aw = "Threshold is met. You earned "+str(Constants.value_high)+" tokens from Group Account A."
        # Bw = "Threshold is met. You earned "+str(Constants.value_low)+" tokens from Group Account B."
        # Al = "Threshold has not been met. You did not earn any tokens from Group Account A."
        # Bl = "Threshold has not been met. You did not earn any tokens from Group Account B."
        
        # calculate the amount of tokens the player has left over
        kept = d['base_tokens']-self.player.contribution_acc_a-self.player.contribution_acc_b
        
        # set up the return vars
        for pl in players:
            pl.acc_a_total=int(groupConA)
            pl.thresh_a_met = bool(groupConA>=d['threshold_high'])
            pl.acc_b_total=int(groupConB)
            pl.thresh_b_met = bool(groupConB>=d['threshold_low'])
        
        lostHigh = 0 if groupConA>=d['threshold_high'] else 1
        AEarn = d['value_high'] if self.player.thresh_a_met else 0
        lostLow = 0 if groupConB>=d['threshold_low'] else 1
        BEarn = d['value_low'] if self.player.thresh_b_met else 0
        
        # save the payoff to the datasheet otherwise it's lost to the void
        self.player.payoff = kept+AEarn+BEarn

        #save to participant vars
        self.player.participant.vars['vars_json_dump']['Game-id_in_group-'+str(self.round_number)]=self.player.id_in_group
        self.player.participant.vars['vars_json_dump']['Game-_id_in_subsesion-'+str(self.round_number)]=self.player.group.id_in_subsession
        self.player.participant.vars['vars_json_dump']['Game-acc_a_total-'+str(self.round_number)]=int(self.player.acc_a_total)
        self.player.participant.vars['vars_json_dump']['Game-acc_b_total-'+str(self.round_number)]=int(self.player.acc_b_total)
        self.player.participant.vars['vars_json_dump']['Game-thresh_a_met-'+str(self.round_number)]=self.player.thresh_a_met
        self.player.participant.vars['vars_json_dump']['Game-thresh_b_met-'+str(self.round_number)]=self.player.thresh_b_met
        self.player.participant.vars['vars_json_dump']['Game-payoff-'+str(self.round_number)]=int(self.player.payoff)
        return dict(
            d,
            all_vars = self.participant.vars,
            dropped=dropped,
            roundNum = self.round_number, 
            lostHigh = lostHigh, 
            lostLow = lostLow,
            groupConA = groupConA-self.player.contribution_acc_a,
            groupConB = groupConB-self.player.contribution_acc_b,
            totConA = groupConA,
            totConB = groupConB,
            kept = kept,
            AEarn = AEarn,
            BEarn = BEarn,
            TotEarn = kept+AEarn+BEarn,
            )
    def before_next_page(self):
        #If it's the last round save the data to the participant otherwise 
        #we won't be able to access it in the next app
        if(self.player.round_number==self.player.TreatmentVars()['total_rounds']):
            self.participant.vars['GameRounds']=[pl.payoff for pl in self.player.in_all_rounds()]
            self.participant.vars['a_total']=[pl.acc_a_total for pl in self.player.in_all_rounds()]
            self.participant.vars['b_total']=[pl.acc_b_total for pl in self.player.in_all_rounds()]
    def app_after_this_page(self,upcoming_apps):
        if self.participant.vars.get('groupmate_timed_out', None)==True or self.player.round_number==self.player.TreatmentVars()['total_rounds']:
            return upcoming_apps[0]

page_sequence = [GroupWaitAsyncGame, GroupWaitSyncGame, p1Game, SeqWait, p2Game, SeqWait, p3Game, SimGame, ResWait, Results]
