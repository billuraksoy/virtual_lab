# from otree.api import Currency as c, currency_range
# from . import pages
# from ._builtin import Bot
# from .models import Constants
from otree.bots import Bot
from otree.bots.bot import ParticipantBot
from otree.bots.runner import SessionBotRunner
#need to add these to requirements
import numpy as np 
#import cv2
#import pyautogui #for screenshots
#import time #for sleep
#import PIL #used by pyautogui
#import imgkit #for convert html to img
from pathlib import Path#


class SBot(Bot):
    def snap(self):
        if hasattr(self,'player'):
            if self.player.TreatmentVars()['screenshot']:
                if self.player.id_in_subsession==self.player.session.config['followed_player'] and self.player.round_number==1:
                    #time.sleep(.5)
                    page=str(self.player.participant._index_in_pages)
                    #print(self.html)
                    mypath = Path().absolute()
                    #print(mypath)
                    config = imgkit.config(wkhtmltoimage=str(mypath)+'/HTML/wkhtmltox/bin/wkhtmltoimage.exe')
                    currentPage = open("HTML/"+page+".html", "w")
                    #currentPage.write((self.html).replace("/static/",str(mypath)+"/HTML/static/"))
                    currentPage.write((self.html).replace("/static/","./static/"))
                    currentPage.close()
                    imgkit.from_file("HTML/"+page+".html","Screenshots/"+page+".jpg", config=config)
                    #part_ind=self._participant_code
                    #part_bot = ParticipantBot.objects_get(id=part_ind)
                    #part_bot = SessionBotRunner.bots[part_ind]
                    #html = part_bot._html
                    #print(html)
                    #image = pyautogui.screenshot("Screenshots/"+page+".png")#take a screenshot
                    # found a way to do it without cv2
                    # image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)#convert it into an rgb array
                    # cv2.imwrite(str("Screenshots/"+page+".png"), image)#write it to a png
                    #time.sleep(.5)
                    return 1
        return 0
    def takeScreenshot(self):
        if hasattr(self,'player'):
            print(self.player.id_in_subsession)
            #print(urls.get_urlpatterns())
            #url = urls.get_urlpatterns()
            #page=page.template_name#get current page url
            #page = url.split("/")[-1].split(".")[0]#extract page from url
            if self.player.id_in_subsession==self.player.session.config['followed_player'] and self.player.round_number==1:
                page=str(self.player.participant._index_in_pages)
                image = pyautogui.screenshot()#take a screenshot
                image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)#convert it into an rgb array
                cv2.imwrite(str("Screenshots/"+page+".png"), image)#write it to a png
        return 1