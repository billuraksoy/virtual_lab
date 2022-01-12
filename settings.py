from os import environ

SESSION_CONFIGS = [
    # dict(
    #    name='public_goods',
    #    display_name="Public Goods",
    #    num_demo_participants=3,
    #    app_sequence=['public_goods', 'payment_info']
    # ),
    # dict(
    # 	name ='my_simple_survey',
    # 	num_demo_participants=3,
    # 	app_sequence=['my_simple_survey']
    # ),
    # dict(
    #     name ='my_public_goods',
    #     num_demo_participants=3,
    #     app_sequence=['my_public_goods']
    # ),
    # dict(
    #     name ='my_trust',
    #     num_demo_participants=2,
    #     app_sequence=['my_trust']
    # ),
    # dict(
    #     name='mtpg_sim_large',#Sim=1, ld=1
    #     num_demo_participants=6,
    #     app_sequence=['threshold_public_goods','threshold_public_goods_practice','threshold_public_goods_game','svo','threshold_public_goods_end','timeout'],
    #     consent='global/ConsentForm.pdf',#path to pdf
    #     threshold_high = 10,
    #     threshold_low = 6,
    #     value_high = 10,
    #     value_low = 7,
    #     base_tokens = 5,
    #     increment = 1,
    #     waiting_room_lowerlimit=2,
    #     group_size=2,
    #     simultaneous=1
    #     ),
    # dict(
    #     name='mtpg_sim_small',#Sim=1, ld=0
    #     num_demo_participants=6,
    #     app_sequence=['threshold_public_goods','threshold_public_goods_practice','threshold_public_goods_game','svo','threshold_public_goods_end','timeout'],
    #     consent='global/ConsentForm.pdf',#path to pdf
    #     threshold_high=8,
    #     threshold_low=6,
    #     value_high=10,
    #     value_low=7,
    #     base_tokens = 5,
    #     increment = 1,
    #     waiting_room_lowerlimit=2,
    #     group_size=2,
    #     simultaneous=1
    #     ),
    # dict(
    #     name='mtpg_seq_large',#Sim=0, ld=1
    #     num_demo_participants=6,
    #     app_sequence=['threshold_public_goods','threshold_public_goods_practice','threshold_public_goods_game','svo','threshold_public_goods_end','timeout'],
    #     consent='global/ConsentForm.pdf',#path to pdf
    #     threshold_high = 10,
    #     threshold_low = 6,
    #     value_high = 10,
    #     value_low = 7,
    #     base_tokens = 5,
    #     increment = 1,
    #     waiting_room_lowerlimit=2,
    #     group_size=2,
    #     simultaneous=0
    #     ),
    # dict(
    #     name='mtpg_seq_small',#Sim=0, ld=0
    #     num_demo_participants=6,
    #     app_sequence=['threshold_public_goods','threshold_public_goods_practice','threshold_public_goods_game','svo','threshold_public_goods_end','timeout'],
    #     consent='global/ConsentForm.pdf',#path to pdf
    #     threshold_high=8,
    #     threshold_low=6,
    #     value_high=10,
    #     value_low=7,
    #     base_tokens = 5,
    #     increment = 1,
    #     waiting_room_lowerlimit=2,
    #     group_size=2,
    #     simultaneous=0
    #     ),
    # dict(
    #     name='mtpg_sim_large_group3',#Sim=1, ld=1
    #     num_demo_participants=6,
    #     app_sequence=['threshold_public_goods','threshold_public_goods_practice','threshold_public_goods_game','svo','threshold_public_goods_end','timeout'],
    #     consent='global/ConsentForm.pdf',#path to pdf
    #     threshold_high = 15,
    #     threshold_low = 9,
    #     value_high = 10,
    #     value_low = 7,
    #     base_tokens = 5,
    #     increment = 1,
    #     waiting_room_lowerlimit=3,
    #     group_size=3,
    #     simultaneous=1
    #     ),
    # dict(
    #     name='mtpg_sim_small_group3',#Sim=1, ld=0
    #     num_demo_participants=6,
    #     app_sequence=['threshold_public_goods','threshold_public_goods_practice','threshold_public_goods_game','svo','threshold_public_goods_end','timeout'],
    #     consent='global/ConsentForm.pdf',#path to pdf
    #     threshold_high=12,
    #     threshold_low=9,
    #     value_high=10,
    #     value_low=7,
    #     base_tokens = 5,
    #     increment = 1,
    #     waiting_room_lowerlimit=3,
    #     group_size=3,
    #     simultaneous=1
    #     ),
    # dict(
    #     name='mtpg_seq_large_group3',#Sim=0, ld=1
    #     num_demo_participants=6,
    #     app_sequence=['threshold_public_goods','threshold_public_goods_practice','threshold_public_goods_game','svo','threshold_public_goods_end','timeout'],
    #     consent='global/ConsentForm.pdf',#path to pdf
    #     threshold_high = 15,
    #     threshold_low = 9,
    #     value_high = 10,
    #     value_low = 7,
    #     base_tokens = 5,
    #     increment = 1,
    #     waiting_room_lowerlimit=3,
    #     group_size=3,
    #     simultaneous=0
    #     ),
    # dict(
    #     name='mtpg_seq_small_group3',#Sim=0, ld=0
    #     num_demo_participants=6,
    #     app_sequence=['threshold_public_goods','threshold_public_goods_practice','threshold_public_goods_game','svo','threshold_public_goods_end','timeout'],
    #     consent='global/ConsentForm.pdf',#path to pdf
    #     threshold_high=12,
    #     threshold_low=9,
    #     value_high=10,
    #     value_low=7,
    #     base_tokens = 5,
    #     increment = 1,
    #     waiting_room_lowerlimit=3,
    #     group_size=3,
    #     simultaneous=0
    #     ),
    # dict(
    #     name='svo',
    #     display_name= "Social Value Orientation",
    #     num_demo_participants= 4,
    #     app_sequence=['svo'],
    #     matching='RING',
    #     select_items='FULL',
    #     items_in_random_order=False,
    #     scale=0.1 ,
    #     slider_init='LEFT',
    #     random_payoff='RAND',
    #     precision='INTEGERS',
    #     language='en',
    #     doc="""
    #         Edit the 'matching' parameter to select RING matching or 
    #         RANDOM_DICTATOR matching.</br>
    #         Edit the 'select_items' parameter to whether we use the first six items 
    #         to calculate the payoff (PRIMARY) or the 15 items (FULL).</br>
    #         Edit the 'scale' parameter to scale the slider values.</br>
    #         Edit the 'slider_init' parameter with LEFT, RIGHT, RAND or AVG to initialize the slider.</br>
    #         Edit the 'random_payoff' parameter with RAND or SUM to determine the way to calculate the payoff.</br>
    #         Edit the 'precision' parameter with TWO_DIGITS_AFTER_POINT or INTEGERS.
    #         """
    # )
    dict(
        num_demo_participants=4,
        name='size_sentiments',
        app_sequence=['prolific_id_begin','size_lgbt_intro','size_lgbt_lists','pilot_survey','size_lgbt_survey','prolific_id_end'],

        )
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    #prolific
    p_completion_link = 'xxxxxxxx',
    #screenshot bot
    screenshot=False,
    use_browser_bots=False,
    #svo
    matching='RING',
    select_items='FULL',
    items_in_random_order=False,
    scale=0.1 ,
    slider_init='LEFT',
    random_payoff='RAND',
    precision='INTEGERS',
    language='en',
    #default
    real_world_currency_per_point=1.00, 
    participation_fee=0.00, 
    participation_payment=5,
    #tpg
    decision_timer=60,
    total_rounds=15,#Otree doesn't natively support variable round numbers, there's a number of work arounds but they're all huristics
    synchronous_game=1,
    doc="",
    consent_link="https://billuraksoy.github.io/virtual_lab/information_sheet.pdf"
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True
POINTS_CUSTOM_NAME = 'tokens'
POINTS_DECIMAL_PLACES = 2

ROOMS = [
        dict(
        name='virtual_lab',
        display_name='Virtual Econ Lab'
        ),
        dict(
        name='erl',
        display_name='ERL',
        participant_label_file='_rooms/erl.txt',
        ),
        dict(
        name='erl2',
        display_name='ERL-2',
        participant_label_file='_rooms/erl2.txt',
        ),
        dict(
        name='erl3',
        display_name='ERL-3',
        participant_label_file='_rooms/erl3.txt',
        ),
    ]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = 'mnl#tu13@-kiljv3pk0=-bnowakzhfa$(%74#*ul!06!v7=dsg'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree','custom_templates']
