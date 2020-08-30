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
    dict(
        name='mtpgT0',#Sim=1, ld=1
        num_demo_participants=6,
        app_sequence=['threshold_public_goods','threshold_public_goods_game','threshold_public_goods_end','timeout'],
        consent='global/ConsentForm.pdf',#path to pdf
        threshold_high = 10,
        threshold_low = 6,
        value_high = 10,
        value_low = 7,
        base_tokens = 5,
        increment = 1,
        waiting_room_lowerlimit=2,
        group_size=2
        )
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, 
    participation_fee=0.00, 
    participation_payment=4,
    large_difference_treatment=1,
    simultaneous=1,
    decision_timer=30,
    total_rounds=10,#Otree doesn't natively support variable round numbers, there's a number of work arounds but they're all huristics
    synchronous_game=1,
    doc=""
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True
POINTS_CUSTOM_NAME = 'tokens'

ROOMS = [
    dict(
        name='erl',
        display_name='ERL',
        participant_label_file='_rooms/erl.txt',
        )
    ]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = 'mnl#tu13@-kiljv3pk0=-bnowakzhfa$(%74#*ul!06!v7=dsg'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree','custom_templates']
