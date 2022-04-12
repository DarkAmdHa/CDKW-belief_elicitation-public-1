from os import environ
SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1, participation_fee=0
)
SESSION_CONFIGS = [
    dict(
        name='Urn_Task',
        app_sequence=[
            'belief_task',
        ],
        num_demo_participants=2,
        showupfee=4,
        bsr=1,
        qsr=0,
        flat=0,
        stakeshigh=1,
        stakeshighval=15,
        stakeslowval=1.5,
        stakesflatval=15,
        full_screen=True,
        live_ping=False,
        audio=True,
    ),
    # dict(
    #     name='Choice_List',
    #     app_sequence=[
    #         'risk_elicitation',
    #     ],
    #     num_demo_participants=2,
    #     showupfee=4,
    #     bsr=0,
    #     qsr=1,
    #     flat=0,
    #     stakeshigh=1,
    #     stakeshighval=15,
    #     stakeslowval=1.5,
    #     stakesflatval=15,
    #     full_screen=True,
    #     live_ping=False,
    #     audio=True,
    # ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'
# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = False
# POINTS_CUSTOM_NAME = "tokens"
REAL_WORLD_CURRENCY_DECIMAL_PLACES = 1
DEMO_PAGE_INTRO_HTML = ''
PARTICIPANT_FIELDS = ['is_dropout', 'dropout', 'order1', 'order2',
                      'riskfirst', 'ambiguityfirst',
                      'urn10_color_code1', 'urn10_color_code2', 'urn2_color_code1', 'urn2_color_code2',
                      'prior1', 'prior2', 'prior3', 'prior4', 'prior5', 'prior6',
                      ]
SESSION_FIELDS = []

ROOMS = [
    dict(
        name='cdkw_1',
        display_name='Experiments in Individual Decision Making 1',
        participant_label_file='_rooms/experimenTUM.txt',
    ),
    dict(
        name='cdkw_2',
        display_name='Experiments in Individual Decision Making 2',
        participant_label_file='_rooms/experimenTUM.txt',
    ),
    dict(
        name='cdkw_3',
        display_name='Experiments in Individual Decision Making 3',
        participant_label_file='_rooms/experimenTUM.txt',
    ),
    dict(
        name='cdkw_4',
        display_name='Experiments in Individual Decision Making 4',
        participant_label_file='_rooms/experimenTUM.txt',
    ),
    ]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

SECRET_KEY = 'blahblah'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
