from otree.api import *
import random

c = Currency

doc = """
Your app description
"""

class PageData:
    def __init__(self, list_q, player_model):
        self.list_q = list_q
        self.player_model = player_model
    def __str__(self):
        return str(self.player_model)



class Constants(BaseConstants):
    name_in_url = 'size_lists'
    players_per_group = None
    num_rounds = 1
    #
    # These text lists are pulled from directly. 
    # To change the text on any page change it here and 
    # everything will update dynamically.
    #
    list_of_SI = [
        "I think the law should prohibit employment discrimination against transgender individuals.",#1
        "I would be comfortable with having a transgender manager at work."
    ]
    list_of_lists = [
        [#1A
        "I have personally met the current Pope.",
        "I own a smartphone.",
        "I think recreational marijuana use should be legal.",
        "I would vote for a political candidate who is pro-life (anti-abortion).",
        ],
        [#1B
        "I have personally met the current U.S. President.",
        "I have at least one social media account (e.g., Facebook, Twitter, Instagram).",
        "I would vote for a political candidate who is pro-choice (supports abortion rights).",
        "I think gun control laws should be relaxed."
        ],
        [#2A
        "I can fluently speak at least three languages.",
        "I have a driver’s license.",
        "I think COVID-19 health risks were overstated.",
        "I support the Black Lives Matter movement.",
        ],
        [#2B
        "I have visited more than twenty countries.",
        "I own a car.",
        "I think parents should be able to opt their children out of a COVID-19 school mask mandate.",
        "I think the law should prohibit employment discrimination against African Americans."
        ],
        [#3
        "I usually respond to my emails within 24 hours.",
        "I am concerned that the media in the United States is biased.",
        "Please put seven as your answer below regardless of how many of the others are true for you.",
        "This is because we would like to see whether you are reading each item carefully.",
        "Again, please put seven for your answer below."
        ]
    ]


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
    for player in subsession.get_players(): #get the list of players and randomize for each player.
        player.participant.vars["T1"] = T1 = bool((player.participant.id_in_session%8) & 1)#get the first bit of the number   1 place
        player.participant.vars["G1First"] = G1First = bool((player.participant.id_in_session%8)>>1 & 1)# second bit of the number 2 place
        player.participant.vars["1AFirst"] = AFirst = bool((player.participant.id_in_session%8)>>2 & 1)# third bit of the number  4 place
        #player.participant.vars["2AFirst"] = A2First = bool((player.participant.id_in_session%16)>>3 & 1)# fourth bit of the number 8 place
        
        A1 = PageData(Constants.list_of_lists[0]+([""] if T1 else [Constants.list_of_SI[0]]),  "1A" if T1 else "1AS")
        B1 = PageData(Constants.list_of_lists[1]+([""] if not T1 else [Constants.list_of_SI[0]]), "1B" if not T1 else "1BS")
        A2 = PageData(Constants.list_of_lists[2]+([""] if T1 else [Constants.list_of_SI[1]]), "2A" if T1 else "2AS")
        B2 = PageData(Constants.list_of_lists[3]+([""] if not T1 else [Constants.list_of_SI[1]]), "2B" if not T1 else "2BS")
        G1 = [A1,B1] if AFirst else [B1,A1]
        G2 = [A2,B2] if AFirst else [B2,A2]
        page_list = G1+G2 if G1First else G2+G1
        page_list += [PageData(Constants.list_of_lists[4],"3")]
        player.participant.vars["page_order"] = page_list #copy that list to page order
        player.page_order = "".join([str(p) for p in page_list])
        player.participant.vars["page_ind"] = 0

class Player(BasePlayer):
    page_order = models.StringField()
    number_stated_1A = models.IntegerField(min=0, max=4, label='Please enter the total number of the above statements that are true for you:')
    number_stated_1AS = models.IntegerField(min=0, max=5, label='Please enter the total number of the above statements that are true for you:')
    number_stated_1B = models.IntegerField(min=0, max=4, label='Please enter the total number of the above statements that are true for you:')
    number_stated_1BS = models.IntegerField(min=0, max=5, label='Please enter the total number of the above statements that are true for you:')
    number_stated_2A = models.IntegerField(min=0, max=4, label='Please enter the total number of the above statements that are true for you:')
    number_stated_2AS = models.IntegerField(min=0, max=5, label='Please enter the total number of the above statements that are true for you:')
    number_stated_2B = models.IntegerField(min=0, max=4, label='Please enter the total number of the above statements that are true for you:')
    number_stated_2BS = models.IntegerField(min=0, max=5, label='Please enter the total number of the above statements that are true for you:')
    number_stated_3 = models.IntegerField(min=0, max=10, label='Please enter the total number of the above statements that are true for you:')


class ListPage(Page):
    template_name = "size_lgbt_lists/ListPage.html"
    form_model = 'player'
    @staticmethod
    def get_form_fields(player: Player):
        return ["number_stated_"+player.participant.vars["page_order"][player.participant.vars["page_ind"]].player_model]
        

    @staticmethod
    def vars_for_template(player: Player):
        page_data_obj = player.participant.vars["page_order"][player.participant.vars["page_ind"]]
        (S1,S2,S3,S4,S5) = page_data_obj.list_q
        if str(page_data_obj) !='3':
            if S5:
                temp = page_data_obj.list_q
                random.shuffle(temp)
                (S1,S2,S3,S4,S5) = temp
            else:
                temp = page_data_obj.list_q[:4]
                random.shuffle(temp)
                (S1,S2,S3,S4) = temp

        return dict(
            S1 = S1,
            S2 = S2,
            S3 = S3,
            S4 = S4,
            S5 = S5
        )
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.vars["page_ind"] += 1

class ListPage1(ListPage):
    pass
class ListPage2(ListPage):
    pass
class ListPage3(ListPage):
    pass
class ListPage4(ListPage):
    pass
class ConstantPage(ListPage):
    pass

page_sequence = [ListPage1, ListPage2, ListPage3, ListPage4, ConstantPage]
