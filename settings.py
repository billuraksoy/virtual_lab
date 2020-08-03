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
        name='threshold_public_goods',
        num_demo_participants=3,
        app_sequence=['threshold_public_goods'],
        consent='ConsentForm.pdf',#path to pdf
        threshold_high = 60,
        threshold_low = 20,
        value_high = 60,
        value_low = 30,
        total_rounds = 10,
        group_size = 3,
        decision_timer=30,
        waiting_room_lowerlimit=3,
        simultaneous = 1,
        base_tokens = 20,
        increment = 10
        )
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = []

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = 'mnl#tu13@-kiljv3pk0=-bnowakzhfa$(%74#*ul!06!v7=dsg'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree','custom_templates']
