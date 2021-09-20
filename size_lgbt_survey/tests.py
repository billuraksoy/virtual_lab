from otree.api import Currency as c, currency_range
from . import *
from otree.api import Bot

from custom_templates.custom_funcs import snap

class PlayerBot(Bot):
    def play_round(self):
        #snap(self)
        yield survey_intro#, dict(promised=1)
        #snap(self)
        yield survey_intro_2
        yield SurveyPage1, dict(Hl=False,age=0,marital=0)
        yield SurveyPage2, dict(occupants=0,children=0,education=0,employment=0)
        yield SurveyPage3, dict(community=0,state="New York",early_state = "New York")
        yield SurveyPage4, dict(trans_manager=False,trans_emp_disc=False)
        yield SurveyPage5, dict(trans_house_disc=False, trans_neighbor=False)
        yield SurveyPage6, dict(gay_manager=False, gay_emp_disc=False, gay_house_disc=False, gay_neighbor=False)
        yield SurveyPage7, dict(your_sex="Male",straight=False,sexuality=0)
        yield SurveyPage8, dict(same_sex=False,attraction=0)
        yield SurveyPage9, dict(religion=0,religion_imp=0)
        yield SurveyPage10, dict(party=0,pol_spectrum=1,pres_2016=0,pres_2020=0)
       	yield SurveyPage11, dict(income=0)
        yield survey_1
        yield SurveyPage13, dict(pop_manager=0,pop_emp=0)