from otree.api import *
import random

c = Currency

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'size_lgbt_lists'
    players_per_group = None
    num_rounds = 3 #number of pages
    page_list = ["1", "2", "3"] #this is because we have three html pages.


class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass


#def creating_session(subsession: Subsession):
#    if subsession.round_number == 1:
#        for player in subsession.get_players(): #get the list of players and randomize for each player.
#            player.participant.page_order = random.shuffle(Constants.page_list)
#            player.page_order = "",join(player.participant.page_order) #this takes the page order, joins them together and puts "" in between. in this case nothing.
            #THIS may not work, CHECK.


def creating_session(subsession: Subsession):
    if subsession.round_number == 1: #if this is the first round, randomize the order
        print("Got here")
        for player in subsession.get_players(): #get the list of players and randomize for each player.
            page_list = [x for x in Constants.page_list] #create a copy of the page_list to be shuffled
            random.shuffle(page_list) #shuffle it in its place
            player.participant.vars["page_order"] = page_list #copy that list to page order
            player.page_order = "".join(list(player.participant.vars["page_order"]))




class Player(BasePlayer):
    page_order = models.StringField()

    number_stated_1 = models.IntegerField(min=0, max=4, label='Please enter the total number of statements above that apply to you:')
    number_stated_2 = models.IntegerField(min=0, max=4, label='Please enter the total number of statements above that apply to you:')
    number_stated_3 = models.IntegerField(min=0, max=10, label='Please enter the total number of statements above that apply to you:')

    sensitive_q_1 = models.IntegerField(
        choices=[[1, 'Yes'], [0, 'No']],
        label="SensitiveQuestion11?",
        widget=widgets.RadioSelect,
    )

    sensitive_q_2 = models.IntegerField(
        choices=[[1, 'Yes'], [0, 'No']],
        label="SensitiveQuestion12?",
        widget=widgets.RadioSelect,
    )

    sensitive_q_3 = models.IntegerField(
        choices=[[1, 'Yes'], [0, 'No']],
        label="SensitiveQuestion12?",
        widget=widgets.RadioSelect,
    )

    sensitive_q_8 = models.IntegerField(
        choices=[[1, 'Yes'], [0, 'No']],
        label="Have you ever travelled outside the country where you currently reside?",
        widget=widgets.RadioSelect,
    )




# PAGES


#class list_1(Page):
#    form_model = 'player'
#    form_fields = ['number_stated_1','sensitive_q_1']


#class list_2(Page):
#    form_model = 'player'
#    3form_fields = ['number_stated_2','sensitive_q_2']


#class list_8(Page):
#    form_model = 'player'
#    form_fields = ['number_stated_8','sensitive_q_8']


class ListPage1(Page):
    template_name = "size_lgbt_lists/ListPage.html"
    form_model = 'player'
    form_fields = ['number_stated_1', 'sensitive_q_1']

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.page_order[player.session.round_number - 1]  == "1"
        # get the page order set up earlier, within that order, get a particular variable. since py starts with zero, in round 1, look at 0
        # round_number is updated across rounds.
        # in round 1, the index is 0
        # in round 2, the index is 1
        # in round 3, the index is 2.

    @staticmethod
    def vars_for_template(player: Player):
        statementList = ["statement11", "statement12", "statement13", "statement14"]
        random.shuffle(statementList)
        (S1, S2, S3, S4) = statementList
        return dict(
            S1 = S1,
            S2 = S2,
            S3 = S3,
            S4 = S4,
        )

    #@staticmethod
    #def vars_for_template(player: Player): #
    #    (S11, S12, S13, S14) = random.shuffle (["Statement11","Statement12","Statement13","Statement14"])
    #    return dict (
    #        S11 = S11,
    #        S12 = S12,
    #        S13 = S13,
    #        S14 = S14,
    #    )


class ListPage2(Page):
    template_name = "size_lgbt_lists/ListPage.html"
    form_model = 'player'
    form_fields = ['number_stated_2','sensitive_q_2']

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.page_order[player.session.round_number - 1]  == "2"


    @staticmethod
    def vars_for_template(player: Player):
        statementList = ["statement21", "statement22", "statement23", "statement24"]
        random.shuffle(statementList)
        (S1, S2, S3, S4) = statementList
        return dict(
            S1 = S1,
            S2 = S2,
            S3 = S3,
            S4 = S4,
        )

class ListPage3(Page):
    template_name = "size_lgbt_lists/ListPage.html"
    form_model = 'player'
    form_fields = ['number_stated_3','sensitive_q_3']

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.page_order[player.session.round_number - 1] == "3"

    @staticmethod
    def vars_for_template(player: Player):
        statementList = ["statement31", "statement32", "statement33", "statement34"]
        random.shuffle(statementList)
        (S1, S2, S3, S4) = statementList
        return dict(
            S1 = S1,
            S2 = S2,
            S3 = S3,
            S4 = S4,
        )

page_sequence = [ListPage1, ListPage2, ListPage3]
