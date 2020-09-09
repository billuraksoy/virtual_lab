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
from otree import common 


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
        players=self.get_players()
        d=players[0].TreatmentVars()
        matrix=[]#fill up a matrix in numerical id order (note, we don't use self.get_matrix here because we want to control group size)
        for a in range(0, len(players), d['group_size']):
            matrix.append(players[a:a+d['group_size']])
        print(matrix)
        self.set_group_matrix(common._group_randomly(matrix, fixed_id_in_group = not d['simultaneous']))

    def group_by_arrival_time_method(self,waiting_players):
        import random
        d=(self.get_players()[0]).TreatmentVars()
        participants = [pl.participant for pl in self.get_players()]#There is no get_participants function for subsession objects
        # a few debug prints
        # print("number of waiting players: "+str(len(waiting_players))) 
        # print("lower limit: "+str(d['waiting_room_lowerlimit']))

        #handles the case where the number of players is less than the lower limit but
        #there are no more players left to wait
        #important to note that this wait page is the first thing that happens in the round -
        #so anyone where round_number is < the waiting players is before them and anyone whose
        #round number is >= the waiting players is after them
        special_case = True
        for partic in participants:
            #if someone hasn't gotten here yet, break because that invalidates the criteria
            if partic._index_in_pages < waiting_players[0].participant._index_in_pages:
                special_case = False
                break
        #if you broke there
        if special_case:
            if len(waiting_players) >= d['group_size']:
                return random.sample(waiting_players,d['group_size'])
            
        #handles the normal case
        if(len(waiting_players)>=d['waiting_room_lowerlimit'] and len(waiting_players) >= d['group_size']):
            #if you've got enough people get a random sample of them and put that into a group
            return random.sample(waiting_players,d['group_size'])




class Group(BaseGroup):
    pass

class fu(BasePlayer):
    def twoPlusTwo():
        return 4

class Player(BasePlayer):
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
    thresh_a_met = models.BooleanField(label="")
    thresh_b_met = models.BooleanField(label="")
