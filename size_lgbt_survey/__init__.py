from otree.api import *
import random

c = Currency

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'size_lgbt_survey'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    #first page
    def make_check_field(label):
        return models.BooleanField(
            label=label,
            widget=widgets.CheckboxInput,
            initial=False,
            blank=True
            )
    Wh = make_check_field("White")
    Bl = make_check_field("Black or African American")
    Na = make_check_field("American Indian or Alaskan Native")
    Ah = make_check_field("Asian or Native Hawaiian or Pacific Islander")
    Ot = make_check_field("Some Other Race")

    def make_yn_field(label):
      return models.BooleanField(
        label = label,
        choices = [[True, 'Yes'], [False, 'No']],
        widget=widgets.RadioSelect
        )

    Hl = make_yn_field("Are you of Hispanic, Latino, or Spanish origin? [American Community Survey]")
    age = models.IntegerField(
      label = "What is your age in years?",
      min=0,
      max=150
      )

    def make_list_field(label,choiceList):
      return models.IntegerField(
        label=label,
        choices = [[i,choiceList[i]] for i in range(len(choiceList))],
        widget=widgets.RadioSelect
        )

    marital = make_list_field("What is your marital status? (choose one) [American Community Survey]", ["Now married","Widowed","Divorced","Separated","Never married"])

    #page 2
    occupants = models.IntegerField( label = "How many people live in your household including yourself", min=0, max=100)
    children = models.IntegerField(label="How many children less than 18 years of age live in your household? If none, please put 0.\n [Behavioral risk factor surveillance system survey, 2018]\nNumber of children:", min= 0, max=100)
    education = make_list_field("What is the highest level of education you've completed? (choose one) (If currently enrolled, mark the previous grade or highest degree received.)", ["High school, GED, or less","Some college credits, no degree","Associate's degree (for example: AA, AS)","Bachelor’s degree or equivalent (for example: BA, BS)","Master’s degree (for example: MA, MS, MEng, MEd, MSW, MBA) or higher (for example: MD, DDS, DVM, LLB, JD, PhD, EdD)"])
    employment = make_list_field("Are you currently…? [Behavioral risk factor surveillance system survey, 2018]",["Employed for wages","Self-employed","Out of work for 1 year or more","Out of work for less than 1 year","A homemaker","A student","Retired","Unable to work"])

    #page 3
    community = make_list_field("What type of community do you live in? [PEW question]",["Rural area","Large city","Small city or town","Suburb near a large city"])
    state = models.StringField(label="In which US state/territory do you currently live?")
    early_state = models.StringField(label="In which US state/territory did you spend the most time for the first 18 years of life?")

    #page 4
    trans_manager = make_yn_field("Would you be comfortable having a transgender manager at work?")
    trans_emp_disc = make_yn_field("Do you think the law should prohibit employment discrimination against transgender individuals?")

    #page 5
    trans_house_disc = make_yn_field("Do you think the law should prohibit housing discrimination against transgender individuals?")
    trans_neighbor = make_yn_field ("Would you be comfortable to have a transgender person as a neighbor?")

    #page 6
    gay_manager = make_yn_field ("Would you be comfortable having an openly lesbian, gay, or bisexual manager at work?")
    gay_emp_disc = make_yn_field ("Do you think the law should prohibit employment discrimination against lesbian, gay, or bisexual individuals?")
    gay_house_disc = make_yn_field ("Do you think the law should prohibit housing discrimination against lesbian, gay, or bisexual individuals?")
    gay_neighbor = make_yn_field ("Would you be comfortable to have an openly lesbian, gay, or bisexual person as a neighbor?")

    #page 7
    #NOTE: Sex at birth is not a binary, should update that.
    your_sex = models.StringField(label="What sex were you assigned at birth, on your original birth certificate? (choose one)", choices=["Male","Female"],widget=widgets.RadioSelect)
    #How do you describe yourself? (check all that apply)
    Ma = make_check_field("Male") 
    Fe = make_check_field("Female")
    Tr = make_check_field("Transgender ")
    Nb = make_check_field("Non-Binary/Other")

    straight = make_yn_field("Are you heterosexual/straight?")
    sexuality = make_list_field("Which of the following best represents how you think of yourself?",["Gay or Lesbian ","Straight, that is, not gay or lesbian","Bisexual","Something else","I don’t know the answer"])

    #page 8
    same_sex = make_yn_field("Since age 18, have you had at least one same-sex sexual partner?")
    #SUGGESTION: Follow up question on romantic attraction since that can differ
    attraction = make_list_field("People are different in their sexual attraction to other people. Which category below best describes your feelings?",["Only attracted to females","Mostly attracted to females","Equally attracted to females and males","Mostly attracted to males","Only attracted to males","None of the above"])

    #Page 9
    religion = make_list_field("What is your religious affiliation?",["Christian (any denomination)","Jewish","Muslim (any denomination)","Hindu","Buddhist ","Asian Folk Religion (e.g., Taoist, Confucian) ","I am not religious ","Some other religious affiliation (please specify below)"])
    religion_oth = models.StringField(label="",blank=True)
    religion_imp = make_list_field("How important is religion in your life?",["Very important","Somewhat important","Not too important","Not at all important"])

    #Page 10
    party = make_list_field("Generally speaking, do you usually think of yourself as a Republican, Democrat, or Independent/Other? Choose the option that best describes you.",["Republican","Democrat","Independent or Other"])
    pol_spectrum = models.IntegerField(
      label = "On a scale of 1-7, 1 being extremely liberal and 7 being extremely conservative, how liberal/conservative would you say your political views on social issues are?",
      choices = [
        [1,"1. Extremely liberal"],
        [2,"2. Liberal"],
        [3,"3. Slightly liberal"],
        [4,"4. Moderate, middle of the road"],
        [5,"5. Slightly conservative"],
        [6,"6. Conservative"],
        [7,"7. Extremely conservative"]
      ],
      widget=widgets.RadioSelect
    )
    pres_2016 = make_list_field("Who did you vote for in the 2016 presidential election?",["Hillary Clinton ","Donald Trump","Other","Did not vote","Not eligible to vote","I do not remember"])
    pres_2020 = make_list_field("Who did you vote for in the 2020 presidential election?",["Joe Biden","Donald Trump","Other","Did not vote","Not eligible to vote","I do not remember"])

    #Page 11
    income = make_list_field("What is your household income before taxes?", ["Less than $20,000","$20,000 - $39,999","$40,000 - $59,999","$60,000 - $79,999","$80,000 - $99,999","$100,000 - $149,999","$150,000 - $199,999","$200,000 or higher"])

    # federal protection question options
    promised = models.IntegerField(#doesn't appear to be used anymore
        choices=[[1, 'Yes'], [0, 'No']],
        label="Do you promise that you will answer the following question without any outside help?",
        widget=widgets.RadioSelect,
    )
    
    disability = models.BooleanField(
        label='Disability',
        widget=widgets.CheckboxInput,
        initial=False,
        blank=True)

    pol_beliefs = models.BooleanField(
        label='Political beliefs/preferences/leaning',
        widget=widgets.CheckboxInput,
        initial=False,
        blank=True)

    race = models.BooleanField(
        label='Race',
        widget=widgets.CheckboxInput,
        initial=False,
        blank=True)

    sexual_orientation = models.BooleanField(
        label='Sexual orientation',
        widget=widgets.CheckboxInput,
        initial=False,
        blank=True)

    eye_color = models.BooleanField(
        label='Eye color',
        widget=widgets.CheckboxInput,
        initial=False,
        blank=True)

    sex = models.BooleanField(
        label='Sex',
        widget=widgets.CheckboxInput,
        initial=False,
        blank=True)

    #page 13
    #In this part of our survey, we want to know what you think about the public perceptions on certain issues in the U.S. When you answer the following questions, please think about the general U.S. population. 
    pop_manager = models.IntegerField(label = "Out of every 100 people in the general US population, I think approximately _____ out of 100 would be comfortable having a transgender manager at work.", min=0, max=100)
    pop_emp = models.IntegerField(label="Out of every 100 people in the general US population, I think approximately _____ out of 100 would agree that the law should prohibit employment discrimination against transgender individuals.", min=0, max=100)







# PAGES
class survey_intro(Page):
    form_model = 'player'
    form_fields = []

class survey_intro_2(Page):
    form_model = 'player'
    form_fields = []

class survey_1(Page):
    form_model = 'player'
    @staticmethod
    def get_form_fields(player: Player):
        fields = ['disability',
                   'pol_beliefs',
                   'race',
                   'sexual_orientation',
                   'eye_color',
                   'sex']
        random.shuffle(fields)
        return fields

class SurveyPage(Page):#template page to make the basic survey pages easier
    template_name = "size_lgbt_survey/Survey_Basic.html"
    form_model = 'player'

class SurveyPage1(Page):
    form_model = 'player'
    form_fields = ["Wh",
                    "Bl",
                    "Na",
                    "Ah",
                    "Ot",
                    "Hl",
                    "age",
                    "marital"]

class SurveyPage2(SurveyPage):
    form_fields=["occupants",
                    "children",
                    "education",
                    "employment"]

class SurveyPage3(SurveyPage):
    form_fields = ["community","state","early_state"]

class SurveyPage4(SurveyPage):
    form_fields = ["trans_manager","trans_emp_disc"]

class SurveyPage5(SurveyPage):
    form_fields = ["trans_house_disc","trans_neighbor"]

class SurveyPage6(SurveyPage):
    form_fields = ["gay_manager","gay_emp_disc","gay_house_disc","gay_neighbor"]

class SurveyPage7(Page):
    form_model = 'player'
    form_fields = ["your_sex","Ma","Fe","Tr","Nb","straight","sexuality"]

class SurveyPage8(SurveyPage):
    form_fields = ["same_sex","attraction"]

class SurveyPage9(SurveyPage):
    form_fields = ["religion","religion_oth","religion_imp"]

class SurveyPage10(SurveyPage):
    form_fields = ["party","pol_spectrum","pres_2016","pres_2020"]

class SurveyPage11(SurveyPage):
    form_fields = ["income"]

#SurveyPage12 is survey_1 since that was developed before the rest of the survey

class SurveyPage13(Page):
    form_model = 'player'
    form_fields = ["pop_manager","pop_emp"]

page_sequence = [survey_intro_2, survey_intro,SurveyPage1,SurveyPage2,SurveyPage3,SurveyPage4,SurveyPage5,SurveyPage6,SurveyPage7,SurveyPage8,SurveyPage9,SurveyPage10,SurveyPage11, survey_1, SurveyPage13]
