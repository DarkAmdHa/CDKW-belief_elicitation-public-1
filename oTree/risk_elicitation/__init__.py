from otree.api import *
import random


doc = """
BSR Ambiguity: Risk Elicitation Task
"""


class Constants(BaseConstants):
    name_in_url = 'risk_elicitation'
    players_per_group = None
    num_rounds = 3
    # risk probabilities
    risk_param = {
        1: 20,
        2: 50,
        3: 80,
    }
    # define set of possible orders of parameters
    risk_order_fixed = [
        [1, 2, 3],
        [1, 3, 2],
        [2, 1, 3],
        [2, 3, 1],
        [3, 1, 2],
        [3, 2, 1],
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # fixed for all rounds
    risk_order = models.IntegerField()
    # parameters specific to round
    risk_prob = models.IntegerField()
    # capture switch point in risk task
    risk_cutoff = models.IntegerField(initial=0)


# FUNCTIONS
def creating_session(subsession: Subsession):
    for player in subsession.get_players():
        # determine order of parameters
        if subsession.round_number == 1:
            player.participant.vars['risk_order'] = random.randint(1, 6)
        player.risk_order = player.participant.vars['risk_order']

        # extract parameters for each round
        risk_orderlist = Constants.risk_order_fixed[player.risk_order - 1]
        player.risk_prob = Constants.risk_param[risk_orderlist[subsession.round_number - 1]]


# PAGES
class WaitPage0(WaitPage):
    wait_for_all_groups = True
    title_text = 'Please wait patiently for the experiment to continue.\
     We will proceed when everyone has completed the task.'
    body_text = ""

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class A_Instructions(Page):

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        session = player.session
        parvars = player.participant.vars

        if session.config['flat'] != 1 & session.config['stakeshigh']:
            player.participant.vars['stakes'] = session.config['stakeshighval']
        elif session.config['flat'] != 1 & session.config['stakeshigh'] != 1:
            player.participant.vars['stakes'] = session.config['stakeslowval']
        elif session.config['flat']:
            player.participant.vars['stakes'] = session.config['stakesflatval']

        return dict(
            par_vars=parvars,
            flat=session.config['flat'],
            stakeshigh=session.config['stakeshigh'],
            stakes=player.participant.vars['stakes'],
            risk_prob=50,
            risk_prob_invert=50,
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        if timeout_happened:
            participant.is_dropout = True
            participant.dropout = "Dropped out at risk task instructions"
        else:
            participant.is_dropout = False

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        if player.participant.is_dropout:
            return upcoming_apps[-1]


class Elicitation(Page):
    form_model = 'player'
    form_fields = ['risk_cutoff']

    @staticmethod
    def vars_for_template(player: Player):
        session = player.session
        parvars = player.participant.vars

        if session.config['flat'] != 1 & session.config['stakeshigh']:
            player.participant.vars['stakes'] = session.config['stakeshighval']
        elif session.config['flat'] != 1 & session.config['stakeshigh'] != 1:
            player.participant.vars['stakes'] = session.config['stakeslowval']
        elif session.config['flat']:
            player.participant.vars['stakes'] = session.config['stakesflatval']

        return dict(
            par_vars=parvars,
            flat=session.config['flat'],
            stakeshigh=session.config['stakeshigh'],
            stakes=player.participant.vars['stakes'],
            risk_prob=player.risk_prob,
            risk_prob_invert=100 - player.risk_prob,
        )

    @staticmethod
    def js_vars(player: Player):
        return dict(
            risk_cutoff=player.risk_cutoff
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.vars['risk_prob_' + str(player.round_number)] = player.risk_prob
        player.participant.vars['risk_cutoff_' + str(player.round_number)] = player.risk_cutoff

        participant = player.participant
        if timeout_happened:
            participant.is_dropout = True
            participant.dropout = "Dropped out at risk elicitation task"
        else:
            participant.is_dropout = False

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        if player.participant.is_dropout:
            return upcoming_apps[-1]


page_sequence = [
    # A_Instructions,
    Elicitation]
