from otree.api import *
import random


doc = """
BSR Ambiguity: Generate Randomization ID Number
"""


class C(BaseConstants):
    NAME_IN_URL = 'randomization_id'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    randomizationID = models.IntegerField()


# FUNCTIONS
def creating_session(subsession: Subsession):
    players = subsession.get_players()
    for player in players:
        player.participant.randomizationID = random.randint(1, 1000)
        # player.participant.randomizationID = random.randint(1, 1)
        player.randomizationID = player.participant.randomizationID


# PAGES
class Randomization_ID(Page):
    @staticmethod
    def vars_for_template(player: Player):
        parvars = player.participant.vars
        session = player.session
        player.participant.is_dropout = False

        if session.config['stakeshigh'] == 1:
            player.participant.vars['stakes'] = session.config['stakeshighval']
        elif session.config['stakeshigh'] == 0:
            player.participant.vars['stakes'] = session.config['stakeslowval']

        if session.config['flat'] == 1:
            player.participant.vars['stakes'] = session.config['stakesflatval']

        return dict(
            par_vars=parvars,
            randomizationfile_locked=session.config['randomizationfile_locked'],
            bsr=session.config['bsr'],
            qsr=session.config['qsr'],
            flat=session.config['flat'],
            stakeshigh=session.config['stakeshigh'],
            stakes=player.participant.vars['stakes'],
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        if timeout_happened:
            participant.is_dropout = True
            participant.dropout = "Dropped out at belief instructions page"

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        if player.participant.is_dropout:
            return upcoming_apps[-1]


page_sequence = [Randomization_ID]
