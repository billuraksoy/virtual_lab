from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)



author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'mtpgg'
    players_per_group=None
    num_rounds = 10


class Subsession(BaseSubsession):
    def after_arrive(self):
        import random
        players=self.get_players()
        #print(players)
        d=players[0].TreatmentVars()
        matrix=[]
        random.shuffle(players)
        #print(players)
        for a in range(0, len(players), d['group_size']):
            matrix.append(players[a:a+d['group_size']])
        #print(matrix)
        self.set_group_matrix(matrix)


    def group_by_arrival_time_method(self,waiting_players):
        import random
        d=(self.get_players()[0]).TreatmentVars()
        # a few debug prints
        # print("number of waiting players: "+str(len(waiting_players))) 
        # print("lower limit: "+str(d['waiting_room_lowerlimit']))
        if(len(waiting_players)>=d['waiting_room_lowerlimit'] and len(waiting_players) >= d['group_size']):
            #if you've got enough people get a random sample of them and put that into a group
            return random.sample(waiting_players,d['group_size'])




class Group(BaseGroup):
    pass


class Player(BasePlayer):
    def TreatmentVars(self):
        # if(self.session.config['synchronous_game']):
        #     N=0
        #     for a in self.session.get_participants():
        #         if a.vars.get('timed_out', None) == False:
        #             if a.vars.get('groupmate_timed_out', False)==False:
        #                 N+=1
        #     wrll=N#in this case the min in waiting room is the number in session
        # else:
        wrll=self.session.config['waiting_room_lowerlimit']
        return dict(
            threshold_high = self.session.config['threshold_high'],
            threshold_low = self.session.config['threshold_low'],
            value_high = self.session.config['value_high'],
            value_low = self.session.config['value_low'],
            total_rounds = self.session.config['total_rounds'],
            group_size = self.session.config['group_size'],
            waiting_room_lowerlimit=wrll,
            simultaneous = self.session.config['simultaneous'],
            base_tokens = self.session.config['base_tokens'],
            increment = self.session.config['increment'],
            decision_timer = self.session.config['decision_timer'],
            participation_payment = self.session.config['participation_payment']
            );

    timed_out_round = models.IntegerField()
    #we don't have to worry about a maximum value here because 
    #the page will error if the total is too high and if we
    #try to base each max off of the base_tokens - the contribution
    #to the other group then that max value is only updated when
    #a submission attempt is made on the form, which leaves you able
    #to softlock yourself out of certain contribution combinations.

    contribution_acc_a = models.CurrencyField(
        min=0,
        initial=0,
        label = "Your Contribution"
        )
    contribution_acc_b = models.CurrencyField(
        min=0,
        initial=0,
        label = "Your Contribution"
        )
    acc_a_total=models.IntegerField(label="")
    acc_b_total=models.IntegerField(label="")