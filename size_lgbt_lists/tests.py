from otree.api import Currency as c, currency_range
from . import *
from otree.api import Bot

from custom_templates.custom_funcs import snap

class PlayerBot(Bot):
    def play_round(self):
        #LON = ["number_stated_1A","number_stated_1AS","number_stated_1B","number_stated_1BS","number_stated_2A","number_stated_2AS","number_stated_2B","number_stated_2BS","number_stated_3"]
        #snap(self)
        d = dict()
        d["number_stated_"+self.player.participant.vars["page_order"][self.player.participant.vars["page_ind"]].player_model]=1
        yield ListPage1, d
        #snap(self)
        d = dict()
        d["number_stated_"+self.player.participant.vars["page_order"][self.player.participant.vars["page_ind"]].player_model]=2
        yield ListPage2,d
        #snap(self)
        d = dict()
        d["number_stated_"+self.player.participant.vars["page_order"][self.player.participant.vars["page_ind"]].player_model]=3
        yield ListPage3,d
        d = dict()
        d["number_stated_"+self.player.participant.vars["page_order"][self.player.participant.vars["page_ind"]].player_model]=4
       	yield ListPage4,d
    
       	yield ConstantPage,dict(number_stated_3=7)
