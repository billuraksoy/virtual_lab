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
from pathlib import Path#needed for snap()

def semantic_diff(html1,html2):#returns weather there is a real semantic difference between two otree pages
    h1=''.join(filter(lambda x: not x.isdigit(), html1.split("<div class=\"card debug-info\">")[0].split("<div class=\"_otree-content\">")[1])) 
    h2=''.join(filter(lambda x: not x.isdigit(), html2.split("<div class=\"card debug-info\">")[0].split("<div class=\"_otree-content\">")[1]))
    print(h1)
    return not h1==h2

def snap(bot):
    if bot.player.TreatmentVars()['screenshot']:
        if bot.player.round_number==1:#only capture the first round
            page = str(bot.player.participant._index_in_pages)
            mypath = Path().absolute()
            curr_html=bot.html.replace("/static/","./static/")#make sure it's able to access the css etc without a django server
            
            if Path("HTML/"+page+".html").is_file():#if there's already an html file here
                currentPage = open("HTML/"+page+".html", "r+")#read it
                old_html = currentPage.read()
                if semantic_diff(old_html,curr_html):#if this page is subject to change on a per player basis
                    currentPage.close()#close the original and open a new one with a hyphen
                    currentPage = open("HTML/"+str(page)+"-"+str(bot.player.id_in_subsession)+".html", "w+")
            else:
                currentPage = open("HTML/"+page+".html","w")#otherwise just make a new file
            currentPage.write(curr_html)#write the html to the file
            currentPage.close()

def TreatmentVars(self):
    if hasattr(self,'session'):#make sure this is only called on things it would work for
        return dict(
            screenshot = self.session.config['screenshot'],
            threshold_high = self.session.config['threshold_high'],
            threshold_low = self.session.config['threshold_low'],
            value_high = self.session.config['value_high'],
            value_low = self.session.config['value_low'],
            total_rounds = self.session.config['total_rounds'],
            group_size = self.session.config['group_size'],
            waiting_room_lowerlimit=self.session.config['waiting_room_lowerlimit'],
            simultaneous = self.session.config['simultaneous'],
            base_tokens = self.session.config['base_tokens'],
            increment = self.session.config['increment'],
            decision_timer = self.session.config['decision_timer'],
            participation_payment = self.session.config['participation_payment']
            );

def participant_vars_dump(self,page):
    pass
    # if self.participant.vars.get('vars_json_dump',None)==None:#if this doesn't exist
    #     self.participant.vars['vars_json_dump']=dict()
    # for field in page.form_fields:
    #     page_name = page.get_template_names()[-1].split("/")[-1].split(".")[0]#in the format "app/page.html" extracts just "page"
    #     self.participant.vars['vars_json_dump'][page_name+'-'+field+('-'+str(self.round_number)) if (not self.round_number==-1) else ""]=str(getattr(self, field))

BasePlayer.TreatmentVars=TreatmentVars
BasePlayer.participant_vars_dump = participant_vars_dump
