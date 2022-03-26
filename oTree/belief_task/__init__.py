from otree.api import *
import random
import itertools


doc = """
BSR Ambiguity: Belief Elicitation Task Instructions
"""


class Constants(BaseConstants):
    name_in_url = 'belief_task'
    players_per_group = None
    num_rounds = 6
    timeout_default = 1800  # Time limit on each page: 30 minutes.
    # composition of urns
    prior_param = {
        1: 20,
        2: 50,
        3: 80,
    }
    # define set of possible orders of parameters
    prior_order_fixed = [
        [1, 2, 3],
        [1, 3, 2],
        [2, 1, 3],
        [2, 3, 1],
        [3, 1, 2],
        [3, 2, 1],
    ]
    # print(urn_order_fixed)
    # define set of possible colors
    color_fixed = {
        1: 'Black',
        2: 'Blue',
        3: 'Green',
        4: 'Cyan',
        5: 'Maroon',
        6: 'Purple',
        7: 'Olive',
        8: 'Gray',
        9: 'Brown',
        10: 'Red',
        11: 'Orange',
        12: 'Pink',
        13: 'Yellow',
        14: 'White',
    }
    # define fixed list to draw colors from
    color_fixed_code = list(range(1, 15))

    # define list of text colors (that would correspond to the list of colors above)
    text_color_fixed = {
        1: 'White',
        2: 'White',
        3: 'White',
        4: 'Black',
        5: 'White',
        6: 'White',
        7: 'White',
        8: 'Black',
        9: 'White',
        10: 'White',
        11: 'Black',
        12: 'Black',
        13: 'Black',
        14: 'Black',
    }


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # fixed for all rounds
    order1 = models.IntegerField(initial=0)
    order2 = models.IntegerField(initial=0)
    riskfirst = models.BooleanField()
    ambiguityfirst = models.BooleanField()

    # parameters specific to round
    treatrisk = models.BooleanField()
    treatambiguity = models.BooleanField()
    prior = models.IntegerField()
    
    # urn color composition in round (index)
    color1 = models.IntegerField()
    color2 = models.IntegerField()
    color3 = models.IntegerField()
    color4 = models.IntegerField()
    color5 = models.IntegerField()

    # number of each colored balls in round
    num_color1 = models.IntegerField(initial=0)
    num_color2 = models.IntegerField(initial=0)
    num_color3 = models.IntegerField(initial=0)
    num_color4 = models.IntegerField(initial=0)
    num_color5 = models.IntegerField(initial=0)

    # color index of predicted event
    color_event = models.IntegerField()
    
    # whether predicting event is true or false
    predict_true = models.BooleanField()
    predict_false = models.BooleanField()
    
    # store decision variable
    belief = models.IntegerField(min=0, max=100, initial=-1)
    cognitive_certainty = models.IntegerField(initial=30)


# FUNCTIONS
def creating_session(subsession: Subsession):
    # set order of parameters within each block of tasks (block 1=rounds 1-3; block 2=rounds 4-6)
    # Note: randomization within each block independent of each other
    # determine whether subject plays ambiguity or risk first
    riskdraw = random.randint(1, 2)
    if riskdraw == 1:
        treatrisk = itertools.cycle([True, False])
    else:
        treatrisk = itertools.cycle([False, True])
    for player in subsession.get_players():
        # determine order of parameters and treatments
        if subsession.round_number == 1:
            player.participant.vars['order1'] = random.randint(1, 6)
            player.participant.vars['order2'] = random.randint(1, 6)
            player.participant.vars['riskfirst'] = next(treatrisk)
            player.participant.vars['ambiguityfirst'] = 1 - player.participant.vars['riskfirst']
        player.order1 = player.participant.vars['order1']
        player.order2 = player.participant.vars['order2']
        player.riskfirst = player.participant.vars['riskfirst']
        player.ambiguityfirst = player.participant.vars['ambiguityfirst']

        # extract risk/ambiguity treatment and parameters for each round
        orderlist1 = Constants.prior_order_fixed[player.order1-1]
        orderlist2 = Constants.prior_order_fixed[player.order2-1]

        if subsession.round_number <= 3:
            player.prior = Constants.prior_param[orderlist1[subsession.round_number-1]]
            player.treatrisk = player.riskfirst
            player.treatambiguity = player.ambiguityfirst

        elif subsession.round_number > 3:
            player.prior = Constants.prior_param[orderlist2[subsession.round_number-4]]
            player.treatrisk = 1 - player.riskfirst
            player.treatambiguity = 1 - player.ambiguityfirst

        # randomize list of urn colors
        if subsession.round_number == 1:
            color_fixed_code_copy = Constants.color_fixed_code.copy()
            urn5_color_code1 = random.sample(color_fixed_code_copy, 5)
            color_fixed_code_copy = [x for x in color_fixed_code_copy if x not in urn5_color_code1]
            urn5_color_code2 = random.sample(color_fixed_code_copy, 5)
            color_fixed_code_copy = [x for x in color_fixed_code_copy if x not in urn5_color_code2]
            urn2_color_code1 = random.sample(color_fixed_code_copy, 2)
            color_fixed_code_copy = [x for x in color_fixed_code_copy if x not in urn2_color_code1]
            urn2_color_code2 = color_fixed_code_copy
            player.participant.vars['urn5_color_code1'] = urn5_color_code1
            player.participant.vars['urn5_color_code2'] = urn5_color_code2
            player.participant.vars['urn2_color_code1'] = urn2_color_code1
            player.participant.vars['urn2_color_code2'] = urn2_color_code2

        # extract urn color composition for each round
        player.participant.vars['prior' + str(subsession.round_number)] = player.prior
        if (subsession.round_number <= 3) & (player.prior == 50):
            player.color1 = player.participant.vars['urn2_color_code1'][0]
            player.color2 = player.participant.vars['urn2_color_code1'][1]
        elif (subsession.round_number > 3) & (player.prior == 50):
            player.color1 = player.participant.vars['urn2_color_code2'][0]
            player.color2 = player.participant.vars['urn2_color_code2'][1]
        elif (subsession.round_number <= 3) & (player.prior != 50):
            player.color1 = player.participant.vars['urn5_color_code1'][0]
            player.color2 = player.participant.vars['urn5_color_code1'][1]
            player.color3 = player.participant.vars['urn5_color_code1'][2]
            player.color4 = player.participant.vars['urn5_color_code1'][3]
            player.color5 = player.participant.vars['urn5_color_code1'][4]
        elif (subsession.round_number > 3) & (player.prior != 50):
            player.color1 = player.participant.vars['urn5_color_code2'][0]
            player.color2 = player.participant.vars['urn5_color_code2'][1]
            player.color3 = player.participant.vars['urn5_color_code2'][2]
            player.color4 = player.participant.vars['urn5_color_code2'][3]
            player.color5 = player.participant.vars['urn5_color_code2'][4]

        # determine exact urn composition for each round
        if player.treatrisk:
            if player.prior == 50:
                player.num_color1 = 50
                player.num_color2 = 50
            elif player.prior != 50:
                player.num_color1 = 20
                player.num_color2 = 20
                player.num_color3 = 20
                player.num_color4 = 20
                player.num_color5 = 20
        if player.treatambiguity:
            if player.prior == 50:
                for x in range(100):
                    # print(x)
                    rollindividualball = random.randint(1, 2)
                    # print(rollindividualball)
                    if rollindividualball == 1:
                        player.num_color1 += 1
                    elif rollindividualball == 2:
                        player.num_color2 += 1
            elif player.prior != 50:
                for x in range(100):
                    # print(x)
                    rollindividualball = random.randint(1, 5)
                    # print(rollindividualball)
                    if rollindividualball == 1:
                        player.num_color1 += 1
                    elif rollindividualball == 2:
                        player.num_color2 += 1
                    elif rollindividualball == 3:
                        player.num_color3 += 1
                    elif rollindividualball == 4:
                        player.num_color4 += 1
                    elif rollindividualball == 5:
                        player.num_color5 += 1

        # randomly draw a color for the Event
        if (subsession.round_number <= 3) & (player.prior == 50):
            player.color_event = player.participant.vars['urn2_color_code1'][random.randint(1, 2) - 1]
        elif (subsession.round_number > 3) & (player.prior == 50):
            player.color_event = player.participant.vars['urn2_color_code2'][random.randint(1, 2) - 1]
        elif (subsession.round_number <= 3) & (player.prior == 20):
            player.color_event = player.participant.vars['urn5_color_code1'][random.randint(1, 3) - 1]
        elif (subsession.round_number > 3) & (player.prior == 20):
            player.color_event = player.participant.vars['urn5_color_code2'][random.randint(1, 2) - 1]
        elif (subsession.round_number <= 3) & (player.prior == 80):
            player.color_event = player.participant.vars['urn5_color_code1'][random.randint(4, 5) - 1]
        elif (subsession.round_number > 3) & (player.prior == 80):
            player.color_event = player.participant.vars['urn5_color_code2'][random.randint(3, 5) - 1]
        
        # determine whether predicting Event or Not Event
        if player.prior == 20:
            player.predict_true = 1
        elif player.prior == 80:
            player.predict_true = 0
        elif player.prior == 50:
            player.predict_true = 1
        player.predict_false = 1 - player.predict_true


# Dropouts
# def get_timeout_seconds1(player: Player):
#     participant = player.participant
#     if participant.is_dropout:
#         return 1
#     else:
#         return Constants.timeout_default


# PAGES
class Elicitation(Page):
    form_model = 'player'
    form_fields = ['belief']

    @staticmethod
    def vars_for_template(player: Player):
        parvars = player.participant.vars
        session = player.session

        if session.config['flat'] != 1 & session.config['stakeshigh']:
            player.participant.vars['stakes'] = session.config['stakeshighval']
        elif session.config['flat'] != 1 & session.config['stakeshigh'] != 1:
            player.participant.vars['stakes'] = session.config['stakeslowval']
        elif session.config['flat']:
            player.participant.vars['stakes'] = session.config['stakesflatval']

        slicecolor1 = Constants.color_fixed[player.color1]
        slicecolor2 = Constants.color_fixed[player.color2]
        slicecolor3 = 'none'
        slicecolor4 = 'none'
        slicecolor5 = 'none'
        textcolor1 = Constants.text_color_fixed[player.color1]
        textcolor2 = Constants.text_color_fixed[player.color2]
        textcolor3 = 'none'
        textcolor4 = 'none'
        textcolor5 = 'none'

        if player.prior != 50:
            slicecolor3 = Constants.color_fixed[player.color3]
            slicecolor4 = Constants.color_fixed[player.color4]
            slicecolor5 = Constants.color_fixed[player.color5]
            textcolor3 = Constants.text_color_fixed[player.color3]
            textcolor4 = Constants.text_color_fixed[player.color4]
            textcolor5 = Constants.text_color_fixed[player.color5]

        if player.treatambiguity:
            textcolor1 = 'black'
            textcolor2 = 'black'
            textcolor3 = 'black'
            textcolor4 = 'black'
            textcolor5 = 'black'

        return dict(
            par_vars=parvars,
            bsr=session.config['bsr'],
            qsr=session.config['qsr'],
            flat=session.config['flat'],
            stakeshigh=session.config['stakeshigh'],
            stakes=player.participant.vars['stakes'],
            slicecolor1=slicecolor1,
            slicecolor2=slicecolor2,
            slicecolor3=slicecolor3,
            slicecolor4=slicecolor4,
            slicecolor5=slicecolor5,
            textcolor1=textcolor1,
            textcolor2=textcolor2,
            textcolor3=textcolor3,
            textcolor4=textcolor4,
            textcolor5=textcolor5,
            numcolor1=player.num_color1,
            numcolor2=player.num_color2,
            numcolor3=player.num_color3,
            numcolor4=player.num_color4,
            numcolor5=player.num_color5,
            prior=player.prior,
            colorevent=Constants.color_fixed[player.color_event],
            treatambiguity=player.treatambiguity,
            treatrisk=player.treatrisk,
            predicttrue=player.predict_true,
            predictfalse=player.predict_false,
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.vars['urn_num_color' + str(player.round_number)] = [player.num_color1, player.num_color2, player.num_color3, player.num_color4, player.num_color5]
        player.participant.vars['treatambiguity' + str(player.round_number)] = player.treatambiguity
        player.participant.vars['treatrisk' + str(player.round_number)] = player.treatrisk
        player.participant.vars['colorevent'+str(player.round_number)] = player.color_event
        player.participant.vars['belief'+str(player.round_number)] = player.belief
        player.participant.vars['predicttrue'+str(player.round_number)] = player.predict_true
        player.participant.vars['predictfalse'+str(player.round_number)] = player.predict_false

        participant = player.participant
        if timeout_happened:
            participant.is_dropout = True
            participant.dropout = "Dropped out at belief elicitation task"
        else:
            participant.is_dropout = False

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        if player.participant.is_dropout:
            return upcoming_apps[-1]


class CognitiveUncertainty(Page):
    form_model = 'player'
    form_fields = ['cognitive_certainty']

    @staticmethod
    def vars_for_template(player: Player):
        parvars = player.participant.vars
        session = player.session

        slicecolor1 = Constants.color_fixed[player.color1]
        slicecolor2 = Constants.color_fixed[player.color2]
        slicecolor3 = 'none'
        slicecolor4 = 'none'
        slicecolor5 = 'none'
        textcolor1 = Constants.text_color_fixed[player.color1]
        textcolor2 = Constants.text_color_fixed[player.color2]
        textcolor3 = 'none'
        textcolor4 = 'none'
        textcolor5 = 'none'

        if player.prior != 50:
            slicecolor3 = Constants.color_fixed[player.color3]
            slicecolor4 = Constants.color_fixed[player.color4]
            slicecolor5 = Constants.color_fixed[player.color5]
            textcolor3 = Constants.text_color_fixed[player.color3]
            textcolor4 = Constants.text_color_fixed[player.color4]
            textcolor5 = Constants.text_color_fixed[player.color5]

        if player.treatambiguity:
            textcolor1 = 'black'
            textcolor2 = 'black'
            textcolor3 = 'black'
            textcolor4 = 'black'
            textcolor5 = 'black'

        return dict(
            par_vars=parvars,
            bsr=session.config['bsr'],
            qsr=session.config['qsr'],
            flat=session.config['flat'],
            stakeshigh=session.config['stakeshigh'],
            stakes=player.participant.vars['stakes'],
            slicecolor1=slicecolor1,
            slicecolor2=slicecolor2,
            slicecolor3=slicecolor3,
            slicecolor4=slicecolor4,
            slicecolor5=slicecolor5,
            textcolor1=textcolor1,
            textcolor2=textcolor2,
            textcolor3=textcolor3,
            textcolor4=textcolor4,
            textcolor5=textcolor5,
            numcolor1=player.num_color1,
            numcolor2=player.num_color2,
            numcolor3=player.num_color3,
            numcolor4=player.num_color4,
            numcolor5=player.num_color5,
            prior=player.prior,
            colorevent=Constants.color_fixed[player.color_event],
            treatambiguity=player.treatambiguity,
            treatrisk=player.treatrisk,
            predicttrue=player.predict_true,
            predictfalse=player.predict_false,
            belief=player.belief,
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.vars['cognitivecertainty' + str(player.round_number)] = player.cognitive_certainty

        participant = player.participant
        if timeout_happened:
            participant.is_dropout = True
            participant.dropout = "Dropped out at belief elicitation task"
        else:
            participant.is_dropout = False

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        if player.participant.is_dropout:
            return upcoming_apps[-1]


page_sequence = [Elicitation, CognitiveUncertainty]
