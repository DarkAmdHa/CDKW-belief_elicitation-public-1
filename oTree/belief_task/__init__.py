from otree.api import *
import csv


doc = """
BSR Ambiguity: Belief Elicitation Task
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
    # define set of possible colors (first 12 are for risky urns)
    color_fixed = {
        1: 'Black',
        2: 'Gray',
        3: 'White',
        4: 'Blue',
        5: 'Cyan',
        6: 'Pink',
        7: 'Red',
        8: 'Purple',
        9: 'Orange',
        10: 'Yellow',
        11: 'Magenta',
        12: 'Green',
        13: 'Maroon',
        14: 'Olive',
        15: 'Aqua',
        16: 'Brown',
        17: 'Indigo',
        18: 'Teal',
        19: 'Turquoise',
        20: 'Beige',
        21: 'Violet',
        22: 'Lavender',
        23: 'Khaki',
        24: 'Lime',
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
    # cognitive_certainty = models.IntegerField(initial=100)
    cognitive_certainty = models.IntegerField(
        widget=widgets.RadioSelect,
        label='',
        choices=[
            [0, '0%'],
            [5, '5%'],
            [10, '10%'],
            [15, '15%'],
            [20, '20%'],
            [25, '25%'],
            [30, '30%'],
            [35, '35%'],
            [40, '40%'],
            [45, '45%'],
            [50, '50%'],
            [55, '55%'],
            [60, '60%'],
            [65, '65%'],
            [70, '70%'],
            [75, '75%'],
            [80, '80%'],
            [85, '85%'],
            [90, '90%'],
            [95, '95%'],
            [100, '100%'],
        ]
    )

    # toggle page number
    belief_subpage = models.IntegerField(initial=1)


# FUNCTIONS
def creating_session(subsession: Subsession):
    # set order of parameters within each block of tasks (block 1=rounds 1-3; block 2=rounds 4-6)
    # Note: randomization within each block independent of each other

    # Import randomization.csv file here
    with open(subsession.session.config['randomizationfile'], encoding='utf-8-sig') as randomizationfile:
        randomizationlist = list(csv.DictReader(randomizationfile))
    # extract all entries
    subsession.session.vars['randomizationlist'] = randomizationlist.copy()

    for player in subsession.get_players():
        # extract randomization data
        randomization_data = [x for x in player.session.vars['randomizationlist'] if x["participant.id_in_session"] == \
                              str(player.participant.randomizationID)]

        # determine order of parameters and treatments
        if subsession.round_number == 1:
            player.participant.vars['order1'] = int(randomization_data[0]['randomization.1.player.order1'])
            player.participant.vars['order2'] = int(randomization_data[0]['randomization.1.player.order2'])
            player.participant.vars['ambiguityfirst'] = player.session.config['ambiguityfirst']
            player.participant.vars['riskfirst'] = 1 - player.participant.vars['ambiguityfirst']
        player.order1 = player.participant.vars['order1']
        player.order2 = player.participant.vars['order2']
        player.ambiguityfirst = player.participant.vars['ambiguityfirst']
        player.riskfirst = player.participant.vars['riskfirst']

        # extract risk/ambiguity treatment and parameters for each round
        orderlist1 = Constants.prior_order_fixed[player.order1 - 1]
        orderlist2 = Constants.prior_order_fixed[player.order2 - 1]

        if subsession.round_number <= 3:
            player.prior = Constants.prior_param[orderlist1[subsession.round_number - 1]]
            player.treatrisk = player.riskfirst
            player.treatambiguity = player.ambiguityfirst

        elif subsession.round_number > 3:
            player.prior = Constants.prior_param[orderlist2[subsession.round_number - 4]]
            player.treatrisk = 1 - player.riskfirst
            player.treatambiguity = 1 - player.ambiguityfirst

        # randomize list of urn colors
        if subsession.round_number == 1:
            # divide set of 24 colors into 2 sets of 5, 5, 2 colors
            player.participant.risky_urn5_color_code1 = \
            list(map(int, list(((randomization_data[0]['participant.risky_urn5_color_code1'].replace('[', '')).replace(']', '')).replace(',', ' ').split())))
            player.participant.risky_urn5_color_code2 = \
            list(map(int, list(((randomization_data[0]['participant.risky_urn5_color_code2'].replace('[', '')).replace(']', '')).replace(',', ' ').split())))
            player.participant.risky_urn2_color_code = \
            list(map(int, list(((randomization_data[0]['participant.risky_urn2_color_code'].replace('[', '')).replace(']', '')).replace(',', ' ').split())))

            player.participant.amb1_urn5_color_code1 = \
            list(map(int, list(((randomization_data[0]['participant.amb1_urn5_color_code1'].replace('[', '')).replace(']', '')).replace(',', ' ').split())))
            player.participant.amb1_urn5_color_code2 = \
            list(map(int, list(((randomization_data[0]['participant.amb1_urn5_color_code2'].replace('[', '')).replace(']', '')).replace(',', ' ').split())))
            player.participant.amb1_urn2_color_code = \
            list(map(int, list(((randomization_data[0]['participant.amb1_urn2_color_code'].replace('[', '')).replace(']', '')).replace(',', ' ').split())))

        # extract urn color composition for each round
        player.participant.vars['prior' + str(subsession.round_number)] = player.prior
        if player.treatrisk & (player.prior == 50):
            player.color1 = player.participant.risky_urn2_color_code[0]
            player.color2 = player.participant.risky_urn2_color_code[1]
        elif player.treatrisk & (player.prior == 20):
            player.color1 = player.participant.risky_urn5_color_code1[0]
            player.color2 = player.participant.risky_urn5_color_code1[1]
            player.color3 = player.participant.risky_urn5_color_code1[2]
            player.color4 = player.participant.risky_urn5_color_code1[3]
            player.color5 = player.participant.risky_urn5_color_code1[4]
        elif player.treatrisk & (player.prior == 80):
            player.color1 = player.participant.risky_urn5_color_code2[0]
            player.color2 = player.participant.risky_urn5_color_code2[1]
            player.color3 = player.participant.risky_urn5_color_code2[2]
            player.color4 = player.participant.risky_urn5_color_code2[3]
            player.color5 = player.participant.risky_urn5_color_code2[4]
        elif player.treatambiguity & (player.prior == 50):
            player.color1 = player.participant.amb1_urn2_color_code[0]
            player.color2 = player.participant.amb1_urn2_color_code[1]
        elif player.treatambiguity & (player.prior == 20):
            player.color1 = player.participant.amb1_urn5_color_code1[0]
            player.color2 = player.participant.amb1_urn5_color_code1[1]
            player.color3 = player.participant.amb1_urn5_color_code1[2]
            player.color4 = player.participant.amb1_urn5_color_code1[3]
            player.color5 = player.participant.amb1_urn5_color_code1[4]
        elif player.treatambiguity & (player.prior == 80):
            player.color1 = player.participant.amb1_urn5_color_code2[0]
            player.color2 = player.participant.amb1_urn5_color_code2[1]
            player.color3 = player.participant.amb1_urn5_color_code2[2]
            player.color4 = player.participant.amb1_urn5_color_code2[3]
            player.color5 = player.participant.amb1_urn5_color_code2[4]

        # determine exact urn composition for each round
        player.participant.risky_urn5_num_color1 = \
            list(map(int, list(((randomization_data[0]['participant.risky_urn5_num_color1'].replace('[', '')).replace(']', '')).replace(',', ' ').split())))
        player.participant.risky_urn5_num_color2 = \
            list(map(int, list(((randomization_data[0]['participant.risky_urn5_num_color2'].replace('[', '')).replace(']', '')).replace(',', ' ').split())))
        player.participant.risky_urn2_num_color = \
            list(map(int, list(((randomization_data[0]['participant.risky_urn2_num_color'].replace('[', '')).replace(']', '')).replace(',', ' ').split())))

        player.participant.amb1_urn5_num_color1 = \
            list(map(int, list(((randomization_data[0]['participant.amb1_urn5_num_color1'].replace('[', '')).replace(']', '')).replace(',', ' ').split())))
        player.participant.amb1_urn5_num_color2 = \
            list(map(int, list(((randomization_data[0]['participant.amb1_urn5_num_color2'].replace('[', '')).replace(']', '')).replace(',', ' ').split())))
        player.participant.amb1_urn2_num_color = \
            list(map(int, list(((randomization_data[0]['participant.amb1_urn2_num_color'].replace('[', '')).replace(']', '')).replace(',', ' ').split())))

        if player.treatrisk:
            if player.prior == 50:
                player.num_color1 = player.participant.risky_urn2_num_color[0]
                player.num_color2 = player.participant.risky_urn2_num_color[1]
            elif player.prior == 20:
                player.num_color1 = player.participant.risky_urn5_num_color1[0]
                player.num_color2 = player.participant.risky_urn5_num_color1[1]
                player.num_color3 = player.participant.risky_urn5_num_color1[2]
                player.num_color4 = player.participant.risky_urn5_num_color1[3]
                player.num_color5 = player.participant.risky_urn5_num_color1[4]
            elif player.prior == 80:
                player.num_color1 = player.participant.risky_urn5_num_color2[0]
                player.num_color2 = player.participant.risky_urn5_num_color2[1]
                player.num_color3 = player.participant.risky_urn5_num_color2[2]
                player.num_color4 = player.participant.risky_urn5_num_color2[3]
                player.num_color5 = player.participant.risky_urn5_num_color2[4]
        if player.treatambiguity:
            if player.prior == 50:
                player.num_color1 = player.participant.amb1_urn2_num_color[0]
                player.num_color2 = player.participant.amb1_urn2_num_color[1]
            elif player.prior == 20:
                player.num_color1 = player.participant.amb1_urn5_num_color1[0]
                player.num_color2 = player.participant.amb1_urn5_num_color1[1]
                player.num_color3 = player.participant.amb1_urn5_num_color1[2]
                player.num_color4 = player.participant.amb1_urn5_num_color1[3]
                player.num_color5 = player.participant.amb1_urn5_num_color1[4]
            elif player.prior == 80:
                player.num_color1 = player.participant.amb1_urn5_num_color2[0]
                player.num_color2 = player.participant.amb1_urn5_num_color2[1]
                player.num_color3 = player.participant.amb1_urn5_num_color2[2]
                player.num_color4 = player.participant.amb1_urn5_num_color2[3]
                player.num_color5 = player.participant.amb1_urn5_num_color2[4]

        # randomly draw a color for the Event
        if subsession.round_number == 1:
            player.participant.risky_urn5_colorevent1 = \
                int(randomization_data[0]['randomization.1.player.risky_urn5_colorevent1'])
            player.participant.risky_urn5_colorevent2 = \
                int(randomization_data[0]['randomization.1.player.risky_urn5_colorevent2'])
            player.participant.risky_urn2_colorevent = \
                int(randomization_data[0]['randomization.1.player.risky_urn2_colorevent'])
            player.participant.amb1_urn5_colorevent1 = \
                int(randomization_data[0]['randomization.1.player.amb1_urn5_colorevent1'])
            player.participant.amb1_urn5_colorevent2 = \
                int(randomization_data[0]['randomization.1.player.amb1_urn5_colorevent2'])
            player.participant.amb1_urn2_colorevent = \
                int(randomization_data[0]['randomization.1.player.amb1_urn2_colorevent'])

        if player.treatrisk & (player.prior == 50):
            player.color_event = player.participant.risky_urn2_colorevent
        elif player.treatrisk & (player.prior == 20):
            player.color_event = player.participant.risky_urn5_colorevent1
        elif player.treatrisk & (player.prior == 80):
            player.color_event = player.participant.risky_urn5_colorevent2
        elif player.treatambiguity & (player.prior == 50):
            player.color_event = player.participant.amb1_urn2_colorevent
        elif player.treatambiguity & (player.prior == 20):
            player.color_event = player.participant.amb1_urn5_colorevent1
        elif player.treatambiguity & (player.prior == 80):
            player.color_event = player.participant.amb1_urn5_colorevent2

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
    def get_form_fields(player: Player):
        if player.belief_subpage == 1:
            return ['belief']
        elif player.belief_subpage == 2:
            return ['cognitive_certainty']

    @staticmethod
    def vars_for_template(player: Player):
        parvars = player.participant.vars
        session = player.session

        if session.config['stakeshigh'] == 1:
            player.participant.vars['stakes'] = session.config['stakeshighval']
        elif session.config['stakeshigh'] == 0:
            player.participant.vars['stakes'] = session.config['stakeslowval']

        if session.config['flat'] == 1:
            player.participant.vars['stakes'] = session.config['stakesflatval']

        slicecolor1 = Constants.color_fixed[player.color1]
        slicecolor2 = Constants.color_fixed[player.color2]
        slicecolor3 = 'none'
        slicecolor4 = 'none'
        slicecolor5 = 'none'

        if player.prior != 50:
            slicecolor3 = Constants.color_fixed[player.color3]
            slicecolor4 = Constants.color_fixed[player.color4]
            slicecolor5 = Constants.color_fixed[player.color5]

        minvalue = player.belief-1
        maxvalue = player.belief+1
        if minvalue < 0:
            minvalue = 0
        if maxvalue > 100:
            maxvalue = 100

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
            uncertaintymin=min(player.belief-0, 100-player.belief),
            video1path=session.config['video1link'],
            video2path=session.config['video2link'],
            video3path=session.config['video3link'],
            minvalue=minvalue,
            maxvalue=maxvalue,
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.belief_subpage == 2:
            player.participant.vars['urn_num_color' + str(player.round_number)] = [player.num_color1,
                                                                                   player.num_color2,
                                                                                   player.num_color3,
                                                                                   player.num_color4,
                                                                                   player.num_color5]
            player.participant.vars['treatambiguity' + str(player.round_number)] = player.treatambiguity
            player.participant.vars['treatrisk' + str(player.round_number)] = player.treatrisk
            player.participant.vars['colorevent' + str(player.round_number)] = player.color_event
            player.participant.vars['predicttrue' + str(player.round_number)] = player.predict_true
            player.participant.vars['predictfalse' + str(player.round_number)] = player.predict_false
            player.participant.vars['belief' + str(player.round_number)] = player.belief
            player.participant.vars['cognitivecertainty' + str(player.round_number)] = player.cognitive_certainty

        participant = player.participant
        if timeout_happened:
            participant.is_dropout = True
            participant.dropout = "Dropped out at belief elicitation task"
        else:
            participant.is_dropout = False

        player.belief_subpage += 1

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        if player.participant.is_dropout:
            return upcoming_apps[-1]

    @staticmethod
    def js_vars(player):
        return dict(
            simple_instruction=player.session.config['simple_instruction'],
        )

class CognitiveUncertainty(Page):
    pass

    # form_model = 'player'
    # form_fields = ['cognitive_certainty']
    #
    # @staticmethod
    # def vars_for_template(player: Player):
    #     parvars = player.participant.vars
    #     session = player.session
    #
    #     slicecolor1 = Constants.color_fixed[player.color1]
    #     slicecolor2 = Constants.color_fixed[player.color2]
    #     slicecolor3 = 'none'
    #     slicecolor4 = 'none'
    #     slicecolor5 = 'none'
    #
    #     if player.prior != 50:
    #         slicecolor3 = Constants.color_fixed[player.color3]
    #         slicecolor4 = Constants.color_fixed[player.color4]
    #         slicecolor5 = Constants.color_fixed[player.color5]
    #
    #     return dict(
    #         par_vars=parvars,
    #         bsr=session.config['bsr'],
    #         qsr=session.config['qsr'],
    #         flat=session.config['flat'],
    #         stakeshigh=session.config['stakeshigh'],
    #         stakes=player.participant.vars['stakes'],
    #         slicecolor1=slicecolor1,
    #         slicecolor2=slicecolor2,
    #         slicecolor3=slicecolor3,
    #         slicecolor4=slicecolor4,
    #         slicecolor5=slicecolor5,
    #         numcolor1=player.num_color1,
    #         numcolor2=player.num_color2,
    #         numcolor3=player.num_color3,
    #         numcolor4=player.num_color4,
    #         numcolor5=player.num_color5,
    #         prior=player.prior,
    #         colorevent=Constants.color_fixed[player.color_event],
    #         treatambiguity=player.treatambiguity,
    #         treatrisk=player.treatrisk,
    #         predicttrue=player.predict_true,
    #         predictfalse=player.predict_false,
    #         belief=player.belief,
    #     )
    #
    # @staticmethod
    # def before_next_page(player: Player, timeout_happened):
    #     player.participant.vars['cognitivecertainty' + str(player.round_number)] = player.cognitive_certainty
    #
    #     participant = player.participant
    #     if timeout_happened:
    #         participant.is_dropout = True
    #         participant.dropout = "Dropped out at belief elicitation task"
    #     else:
    #         participant.is_dropout = False
    #
    # @staticmethod
    # def app_after_this_page(player: Player, upcoming_apps):
    #     if player.participant.is_dropout:
    #         return upcoming_apps[-1]

page_sequence = [Elicitation, Elicitation]
