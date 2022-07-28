from otree.api import *


doc = """
BSR Ambiguity: Belief Elicitation Task Instructions
"""


class Constants(BaseConstants):
    name_in_url = 'belief_instructions'
    players_per_group = None
    num_rounds = 1
    timeout_default = 1800  # Time limit on each page: 30 minutes.
    comprehension_timeout = 0  # Time limit before comprehension questions appear (in ms)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    ctrlqns_exptaskpayment = models.BooleanField(
        choices=[
            [1, "True"],
            [0, "False"],
        ],
        widget=widgets.RadioSelect,
    )

    ctrlqns_beliefroundpayment = models.BooleanField(
        choices=[
            [1, "True"],
            [0, "False"],
        ],
        widget=widgets.RadioSelect,
    )

    ctrlqns_beliefcalc_event = models.FloatField()

    ctrlqns_beliefcalc_notevent = models.FloatField()

    ctrlqns_video1_heart0 = models.IntegerField()
    ctrlqns_video1_heart25 = models.IntegerField()
    ctrlqns_video1_heart75 = models.IntegerField()
    ctrlqns_video1_heart100 = models.IntegerField()

    ctrlqns_video2_notheart0 = models.IntegerField()
    ctrlqns_video2_notheart25 = models.IntegerField()
    ctrlqns_video2_notheart75 = models.IntegerField()
    ctrlqns_video2_notheart100 = models.IntegerField()

    ctrlqns_video3_average_max = models.IntegerField()
    ctrlqns_video3_average0 = models.FloatField()
    ctrlqns_video3_average25 = models.FloatField()
    ctrlqns_video3_average75 = models.FloatField()
    ctrlqns_video3_average100 = models.FloatField()

    ctrlclicks_exptaskpayment = models.IntegerField(initial=0)
    ctrlclicks_beliefroundpayment = models.IntegerField(initial=0)
    ctrlclicks_beliefcalc_event = models.IntegerField(initial=0)
    ctrlclicks_beliefcalc_notevent = models.IntegerField(initial=0)

    ctrlclicks_video1_heart0 = models.IntegerField(initial=0)
    ctrlclicks_video1_heart25 = models.IntegerField(initial=0)
    ctrlclicks_video1_heart75 = models.IntegerField(initial=0)
    ctrlclicks_video1_heart100 = models.IntegerField(initial=0)

    ctrlclicks_video2_notheart0 = models.IntegerField(initial=0)
    ctrlclicks_video2_notheart25 = models.IntegerField(initial=0)
    ctrlclicks_video2_notheart75 = models.IntegerField(initial=0)
    ctrlclicks_video2_notheart100 = models.IntegerField(initial=0)

    ctrlclicks_video3_average_max = models.IntegerField(initial=0)
    ctrlclicks_video3_average0 = models.IntegerField(initial=0)
    ctrlclicks_video3_average25 = models.IntegerField(initial=0)
    ctrlclicks_video3_average75 = models.IntegerField(initial=0)
    ctrlclicks_video3_average100 = models.IntegerField(initial=0)

    ctrlclicks_total = models.IntegerField(initial=0)

    understanding_certainty = models.IntegerField()

    compqns_payment_det = models.IntegerField(
        widget=widgets.RadioSelect,
        label="What statement best reflects the payment procedure?<br><br>",
        choices=[
            [1, "My payment depends both on the outcome of the event and my prediction."],
            [2, "My payment depends only on my prediction, and not on the outcome of the event."],
        ],
    )

    compqns_optimal_belief0 = models.IntegerField(
        label="If you knew that an event was not going to happen for sure, \
        what would be the prediction that would maximize your chances of receiving the payment?<br><br>",
        min=0,
        max=100,
    )

    compqns_optimal_belief75 = models.IntegerField(
        label="Imagine that you are predicting the chances that a card drawn \
        from a standard deck of playing cards turns out to be a DIAMOND, CLUB, or SPADE.<br><br>\
        Before knowing the outcome, what is the prediction that would <b>on average</b> give you \
        the highest chance of receiving the payment according to the procedure?<br><br>",
        min=0,
        max=100,
    )

    compqns_payment_optimal = models.IntegerField(
        widget=widgets.RadioSelect,
        label="Which of the following statements best reflects the payment procedure?<br><br>",
        choices=[
            [1, "The payment procedure is designed so that I will earn the most money <b>on average</b> \
            if I enter my true prediction of a given event."],
            [2, "The payment procedure is designed so that I will earn the most money <b>on average</b> \
            if I enter a prediction of 0% for unlikely events, and 100% for likely events."],
            [3, "The payment procedure is designed so that I will earn the most money <b>on average</b> \
            if I enter a prediction of 50%."],
        ],
    )


# FUNCTIONS
# Dropouts
def get_timeout_seconds1(player: Player):
    participant = player.participant
    if participant.is_dropout:
        return 1
    else:
        return Constants.timeout_default


# PAGES
class WaitPage0(WaitPage):
    wait_for_all_groups = True
    title_text = 'Please wait patiently for the experiment to continue.'
    body_text = ""


# class A_Instructions_Old(Page):
#     form_model = 'player'
#
#     @staticmethod
#     def is_displayed(player: Player):
#         return player.participant.is_dropout is False
#
#     @staticmethod
#     def vars_for_template(player: Player):
#         parvars = player.participant.vars
#         session = player.session
#
#         if session.config['stakeshigh'] == 1:
#             player.participant.vars['stakes'] = session.config['stakeshighval']
#         elif session.config['stakeshigh'] == 0:
#             player.participant.vars['stakes'] = session.config['stakeslowval']
#
#         if session.config['flat'] == 1:
#             player.participant.vars['stakes'] = session.config['stakesflatval']
#
#         return dict(
#             par_vars=parvars,
#             bsr=session.config['bsr'],
#             qsr=session.config['qsr'],
#             flat=session.config['flat'],
#             stakeshigh=session.config['stakeshigh'],
#             stakes=player.participant.vars['stakes'],
#         )
#
#     @staticmethod
#     def before_next_page(player: Player, timeout_happened):
#         participant = player.participant
#         if timeout_happened:
#             participant.is_dropout = True
#             participant.dropout = "Dropped out at belief instructions page"
#
#     @staticmethod
#     def app_after_this_page(player: Player, upcoming_apps):
#         if player.participant.is_dropout:
#             return upcoming_apps[-1]


# class Qns_ExpTaskPayment(Page):
#     form_model = "player"
#     form_fields = ['ctrlqns_exptaskpayment']
#
#     @staticmethod
#     def error_message(player, values):
#         player.ctrlclicks_exptaskpayment += 1
#         solution = 0
#         error_messages = dict()
#         if values['ctrlqns_exptaskpayment'] != solution:
#             error_messages['ctrlqns_exptaskpayment'] = "Your answer is incorrect. \
#             You will be paid for the decisions you make in ONE randomly chosen part of the experiment. \
#             Please try again."
#         return error_messages
#
#     get_timeout_seconds = get_timeout_seconds1
#
#     @staticmethod
#     def before_next_page(player: Player, timeout_happened):
#         player.participant.vars['ctrlattempts_exptaskpayment'] = player.ctrlclicks_exptaskpayment
#         if timeout_happened:
#             participant = player.participant
#             # If dropout occurs, the variable participant.dropout will record when it happened
#             if participant.is_dropout == False:
#                 participant.dropout = "Dropped out at comprehension question 1"
#             participant.is_dropout = True
#
#     @staticmethod
#     def vars_for_template(player: Player):
#         parvars = player.participant.vars
#         return dict(
#             par_vars=parvars
#         )
#
#     @staticmethod
#     def app_after_this_page(player: Player, upcoming_apps):
#         if player.participant.is_dropout:
#             return upcoming_apps[-1]


# class Qns_BeliefRoundPayment(Page):
#     form_model = "player"
#     form_fields = ['ctrlqns_beliefroundpayment']
#
#     @staticmethod
#     def error_message(player, values):
#         player.ctrlclicks_beliefroundpayment += 1
#         solution = 1
#         error_messages = dict()
#         if values['ctrlqns_beliefroundpayment'] != solution:
#             error_messages['ctrlqns_beliefroundpayment'] = "Your answer is incorrect. \
#             You will participate in six rounds of a decision task in Part A. \
#             If you are paid for Part A, you will be paid for your decisions in ONE of the six rounds. \
#             Please try again."
#         return error_messages
#
#     get_timeout_seconds = get_timeout_seconds1
#
#     @staticmethod
#     def before_next_page(player: Player, timeout_happened):
#         player.participant.vars['ctrlattempts_beliefroundpayment'] = player.ctrlclicks_beliefroundpayment
#         if timeout_happened:
#             participant = player.participant
#             # If dropout occurs, the variable participant.dropout will record when it happened
#             if participant.is_dropout == False:
#                 participant.dropout = "Dropped out at comprehension question 2"
#             participant.is_dropout = True
#
#     @staticmethod
#     def vars_for_template(player: Player):
#         parvars = player.participant.vars
#         return dict(
#             par_vars=parvars
#         )
#
#     @staticmethod
#     def app_after_this_page(player: Player, upcoming_apps):
#         if player.participant.is_dropout:
#             return upcoming_apps[-1]


# class Qns_BeliefCalcEvent(Page):
#     form_model = "player"
#     form_fields = ['ctrlqns_beliefcalc_event']
#
#     @staticmethod
#     def error_message(player, values):
#         player.ctrlclicks_beliefcalc_event += 1
#
#         session = player.session
#
#         if session.config['bsr']:
#             solution = (1 - ((100 - 40) / 100) ** 2) * 100
#         elif session.config['qsr'] or session.config['flat']:
#             solution = (1 - ((100 - 40) / 100) ** 2) * player.participant.vars['stakes']
#         error_messages = dict()
#         if values['ctrlqns_beliefcalc_event'] != solution:
#             error_messages['ctrlqns_beliefcalc_event'] = "Your answer is incorrect. \
#             In this instance, the Event OCCURS. \
#             Please apply the correct formula given in the instructions and try again."
#         return error_messages
#
#     get_timeout_seconds = get_timeout_seconds1
#
#     @staticmethod
#     def before_next_page(player: Player, timeout_happened):
#         player.participant.vars['ctrlattempts_beliefcalc_event'] = player.ctrlclicks_beliefcalc_event
#         if timeout_happened:
#             participant = player.participant
#             # If dropout occurs, the variable participant.dropout will record when it happened
#             if participant.is_dropout == False:
#                 participant.dropout = "Dropped out at comprehension question 3"
#             participant.is_dropout = True
#
#     @staticmethod
#     def vars_for_template(player: Player):
#         parvars = player.participant.vars
#         session = player.session
#
#         return dict(
#             par_vars=parvars,
#             bsr=session.config['bsr'],
#             qsr=session.config['qsr'],
#             flat=session.config['flat'],
#             stakeshigh=session.config['stakeshigh'],
#             stakes=player.participant.vars['stakes'],
#         )
#
#     @staticmethod
#     def app_after_this_page(player: Player, upcoming_apps):
#         if player.participant.is_dropout:
#             return upcoming_apps[-1]


# class Qns_BeliefCalcNotEvent(Page):
#     form_model = "player"
#     form_fields = ['ctrlqns_beliefcalc_notevent']
#
#     @staticmethod
#     def error_message(player, values):
#         player.ctrlclicks_beliefcalc_notevent += 1
#
#         session = player.session
#
#         if session.config['bsr']:
#             solution = (1 - (40 / 100) ** 2) * 100
#         elif session.config['qsr'] or session.config['flat']:
#             solution = (1 - (40 / 100) ** 2) * player.participant.vars['stakes']
#         error_messages = dict()
#         if values['ctrlqns_beliefcalc_notevent'] != solution:
#             error_messages['ctrlqns_beliefcalc_notevent'] = "Your answer is incorrect. \
#             In this instance, the Event DOES NOT OCCUR. \
#             Please apply the correct formula given in the instructions and try again."
#         return error_messages
#
#     get_timeout_seconds = get_timeout_seconds1
#
#     @staticmethod
#     def before_next_page(player: Player, timeout_happened):
#         player.participant.vars['ctrlattempts_beliefcalc_notevent'] = player.ctrlclicks_beliefcalc_notevent
#         if timeout_happened:
#             participant = player.participant
#             # If dropout occurs, the variable participant.dropout will record when it happened
#             if participant.is_dropout == False:
#                 participant.dropout = "Dropped out at comprehension question 4"
#             participant.is_dropout = True
#
#         # add total number of clicks across all comprehension questions
#         # player.ctrlclicks_total = player.ctrlclicks_exptaskpayment + player.ctrlclicks_beliefroundpayment + player.\
#         #     ctrlclicks_beliefcalc_event + player.ctrlclicks_beliefcalc_notevent
#         player.participant.vars['ctrlattempts_total'] = player.ctrlclicks_total
#
#     @staticmethod
#     def vars_for_template(player: Player):
#         parvars = player.participant.vars
#         session = player.session
#
#         return dict(
#             par_vars=parvars,
#             bsr=session.config['bsr'],
#             qsr=session.config['qsr'],
#             flat=session.config['flat'],
#             stakeshigh=session.config['stakeshigh'],
#             stakes=player.participant.vars['stakes'],
#         )
#
#     @staticmethod
#     def app_after_this_page(player: Player, upcoming_apps):
#         if player.participant.is_dropout:
#             return upcoming_apps[-1]


class InstructionUncertainty(Page):
    form_model = "player"
    form_fields = ['understanding_certainty']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.vars['understanding_certainty'] = player.understanding_certainty
        if timeout_happened:
            participant = player.participant
            # If dropout occurs, the variable participant.dropout will record when it happened
            if participant.is_dropout == False:
                participant.dropout = "Dropped out at end of comprehension question"
            participant.is_dropout = True

    @staticmethod
    def vars_for_template(player: Player):
        parvars = player.participant.vars
        session = player.session

        return dict(
            par_vars=parvars,
            bsr=session.config['bsr'],
            qsr=session.config['qsr'],
            flat=session.config['flat'],
            stakeshigh=session.config['stakeshigh'],
            stakes=player.participant.vars['stakes'],
        )

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        if player.participant.is_dropout:
            return upcoming_apps[-1]


class WaitPage1(WaitPage):
    wait_for_all_groups = True
    title_text = 'Please wait patiently for the experiment to continue.\
     We will proceed when everyone has finished the comprehension questions.'
    body_text = ""


class AnswerCorrect(Page):

    @staticmethod
    def is_displayed(player):
        return player.session.config['simple_instruction'] is False

    @staticmethod
    def vars_for_template(player: Player):
        parvars = player.participant.vars
        session = player.session

        return dict(
            par_vars=parvars,
            bsr=session.config['bsr'],
            qsr=session.config['qsr'],
            flat=session.config['flat'],
            stakeshigh=session.config['stakeshigh'],
            stakes=player.participant.vars['stakes'],
        )


class EndComprehension(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):
        if player.session.config['instructionpilot'] is False:
            return player.participant.is_dropout is False

    @staticmethod
    def vars_for_template(player: Player):
        parvars = player.participant.vars
        session = player.session

        return dict(
            par_vars=parvars,
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


class A_Video_Overview(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.is_dropout is False

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

        return dict(
            par_vars=parvars,
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


class Instructions_Video_1(Page):
    form_model = "player"
    form_fields = [
        'ctrlqns_video1_heart0',
        'ctrlqns_video1_heart25',
        'ctrlqns_video1_heart75',
        'ctrlqns_video1_heart100',
    ]

    @staticmethod
    def is_displayed(player):
        return player.session.config['simple_instruction'] is False

    @staticmethod
    def error_message(player, values):
        solution_heart0 = round((1 - ((100 - 0) / 100) ** 2) * 100, 0)
        solution_heart25 = round((1 - ((100 - 25) / 100) ** 2) * 100, 0)
        solution_heart75 = round((1 - ((100 - 75) / 100) ** 2) * 100, 0)
        solution_heart100 = round((1 - ((100 - 100) / 100) ** 2) * 100, 0)

        error_messages = dict()
        if values['ctrlqns_video1_heart0'] != solution_heart0:
            player.ctrlclicks_video1_heart0 += 1
            player.ctrlclicks_total += 1
            error_messages['ctrlqns_video1_heart0'] = "Your answer is incorrect. Please try again."
        if values['ctrlqns_video1_heart25'] != solution_heart25:
            player.ctrlclicks_video1_heart25 += 1
            player.ctrlclicks_total += 1
            error_messages['ctrlqns_video1_heart25'] = "Your answer is incorrect. Please try again."
        if values['ctrlqns_video1_heart75'] != solution_heart75:
            player.ctrlclicks_video1_heart75 += 1
            player.ctrlclicks_total += 1
            error_messages['ctrlqns_video1_heart75'] = "Your answer is incorrect. Please try again."
        if values['ctrlqns_video1_heart100'] != solution_heart100:
            player.ctrlclicks_video1_heart100 += 1
            player.ctrlclicks_total += 1
            error_messages['ctrlqns_video1_heart100'] = "Your answer is incorrect. Please try again."
        return error_messages

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.vars['ctrlattempts_video1_heart0'] = player.ctrlclicks_video1_heart0
        player.participant.vars['ctrlattempts_video1_heart25'] = player.ctrlclicks_video1_heart25
        player.participant.vars['ctrlattempts_video1_heart75'] = player.ctrlclicks_video1_heart75
        player.participant.vars['ctrlattempts_video1_heart100'] = player.ctrlclicks_video1_heart100
        player.participant.vars['ctrlattempts_total'] = player.ctrlclicks_total
        if timeout_happened:
            participant = player.participant
            # If dropout occurs, the variable participant.dropout will record when it happened
            if not participant.is_dropout:
                participant.dropout = "Dropped out at end of comprehension question"
            participant.is_dropout = True

    @staticmethod
    def vars_for_template(player: Player):
        parvars = player.participant.vars
        session = player.session

        return dict(
            par_vars=parvars,
            bsr=session.config['bsr'],
            qsr=session.config['qsr'],
            flat=session.config['flat'],
            stakeshigh=session.config['stakeshigh'],
            stakes=player.participant.vars['stakes'],
            video1path=session.config['video1link'],
        )

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        if player.participant.is_dropout:
            return upcoming_apps[-1]


class Instructions_Video_2(Page):
    form_model = "player"
    form_fields = [
        'ctrlqns_video2_notheart0',
        'ctrlqns_video2_notheart25',
        'ctrlqns_video2_notheart75',
        'ctrlqns_video2_notheart100',
    ]

    @staticmethod
    def is_displayed(player):
        return player.session.config['simple_instruction'] is False

    @staticmethod
    def error_message(player, values):
        solution_notheart0 = round((1 - ((0 - 0) / 100) ** 2) * 100, 0)
        solution_notheart25 = round((1 - ((0 - 25) / 100) ** 2) * 100, 0)
        solution_notheart75 = round((1 - ((0 - 75) / 100) ** 2) * 100, 0)
        solution_notheart100 = round((1 - ((0 - 100) / 100) ** 2) * 100, 0)

        error_messages = dict()
        if values['ctrlqns_video2_notheart0'] != solution_notheart0:
            player.ctrlclicks_video2_notheart0 += 1
            player.ctrlclicks_total += 1
            error_messages['ctrlqns_video2_notheart0'] = "Your answer is incorrect. Please try again."
        if values['ctrlqns_video2_notheart25'] != solution_notheart25:
            player.ctrlclicks_video2_notheart25 += 1
            player.ctrlclicks_total += 1
            error_messages['ctrlqns_video2_notheart25'] = "Your answer is incorrect. Please try again."
        if values['ctrlqns_video2_notheart75'] != solution_notheart75:
            player.ctrlclicks_video2_notheart75 += 1
            player.ctrlclicks_total += 1
            error_messages['ctrlqns_video2_notheart75'] = "Your answer is incorrect. Please try again."
        if values['ctrlqns_video2_notheart100'] != solution_notheart100:
            player.ctrlclicks_video2_notheart100 += 1
            player.ctrlclicks_total += 1
            error_messages['ctrlqns_video2_notheart100'] = "Your answer is incorrect. Please try again."
        return error_messages

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.vars['ctrlattempts_video2_notheart0'] = player.ctrlclicks_video2_notheart0
        player.participant.vars['ctrlattempts_video2_notheart25'] = player.ctrlclicks_video2_notheart25
        player.participant.vars['ctrlattempts_video2_notheart75'] = player.ctrlclicks_video2_notheart75
        player.participant.vars['ctrlattempts_video2_notheart100'] = player.ctrlclicks_video2_notheart100
        player.participant.vars['ctrlattempts_total'] = player.ctrlclicks_total
        if timeout_happened:
            participant = player.participant
            # If dropout occurs, the variable participant.dropout will record when it happened
            if not participant.is_dropout:
                participant.dropout = "Dropped out at end of comprehension question"
            participant.is_dropout = True

    @staticmethod
    def vars_for_template(player: Player):
        parvars = player.participant.vars
        session = player.session

        return dict(
            par_vars=parvars,
            bsr=session.config['bsr'],
            qsr=session.config['qsr'],
            flat=session.config['flat'],
            stakeshigh=session.config['stakeshigh'],
            stakes=player.participant.vars['stakes'],
            video2path=session.config['video2link'],
        )

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        if player.participant.is_dropout:
            return upcoming_apps[-1]


class Instructions_Video_3(Page):
    form_model = "player"
    form_fields = [
        'ctrlqns_video3_average_max',
        'ctrlqns_video3_average0',
        'ctrlqns_video3_average25',
        'ctrlqns_video3_average75',
        'ctrlqns_video3_average100',
    ]

    @staticmethod
    def is_displayed(player):
        return player.session.config['simple_instruction'] is False

    @staticmethod
    def error_message(player, values):
        solution_average_max = 25
        solution_average0 = round(
            0.25 * ((1 - ((100 - 0) / 100) ** 2) * 100) + 0.75 * ((1 - ((0 - 0) / 100) ** 2) * 100), 2)
        solution_average25 = round(
            0.25 * ((1 - ((100 - 25) / 100) ** 2) * 100) + 0.75 * ((1 - ((0 - 25) / 100) ** 2) * 100), 2)
        solution_average75 = round(
            0.25 * ((1 - ((100 - 75) / 100) ** 2) * 100) + 0.75 * ((1 - ((0 - 75) / 100) ** 2) * 100), 2)
        solution_average100 = round(
            0.25 * ((1 - ((100 - 100) / 100) ** 2) * 100) + 0.75 * ((1 - ((0 - 100) / 100) ** 2) * 100), 2)

        error_messages = dict()
        if values['ctrlqns_video3_average_max'] != solution_average_max:
            player.ctrlclicks_video3_average_max += 1
            player.ctrlclicks_total += 1
            error_messages['ctrlqns_video3_average_max'] = "Your answer is incorrect. Please try again."
        if round(values['ctrlqns_video3_average0'], 2) != solution_average0:
            player.ctrlclicks_video3_average0 += 1
            player.ctrlclicks_total += 1
            error_messages['ctrlqns_video3_average0'] = "Your answer is incorrect. Please try again."
        if round(values['ctrlqns_video3_average25'], 2) != solution_average25:
            player.ctrlclicks_video3_average25 += 1
            player.ctrlclicks_total += 1
            error_messages['ctrlqns_video3_average25'] = "Your answer is incorrect. Please try again."
        if round(values['ctrlqns_video3_average75'], 2) != solution_average75:
            player.ctrlclicks_video3_average75 += 1
            player.ctrlclicks_total += 1
            error_messages['ctrlqns_video3_average75'] = "Your answer is incorrect. Please try again."
        if round(values['ctrlqns_video3_average100'], 2) != solution_average100:
            player.ctrlclicks_video3_average100 += 1
            player.ctrlclicks_total += 1
            error_messages['ctrlqns_video3_average100'] = "Your answer is incorrect. Please try again."
        return error_messages

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.vars['ctrlattempts_video3_average_max'] = player.ctrlclicks_video3_average_max
        player.participant.vars['ctrlattempts_video3_average0'] = player.ctrlclicks_video3_average0
        player.participant.vars['ctrlattempts_video3_average25'] = player.ctrlclicks_video3_average25
        player.participant.vars['ctrlattempts_video3_average75'] = player.ctrlclicks_video3_average75
        player.participant.vars['ctrlattempts_video3_average100'] = player.ctrlclicks_video3_average100
        player.participant.vars['ctrlattempts_total'] = player.ctrlclicks_total
        if timeout_happened:
            participant = player.participant
            # If dropout occurs, the variable participant.dropout will record when it happened
            if not participant.is_dropout:
                participant.dropout = "Dropped out at end of comprehension question"
            participant.is_dropout = True

    @staticmethod
    def vars_for_template(player: Player):
        parvars = player.participant.vars
        session = player.session

        return dict(
            par_vars=parvars,
            bsr=session.config['bsr'],
            qsr=session.config['qsr'],
            flat=session.config['flat'],
            stakeshigh=session.config['stakeshigh'],
            stakes=player.participant.vars['stakes'],
            video3path=session.config['video3link'],
        )

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        if player.participant.is_dropout:
            return upcoming_apps[-1]


class Instructions_Video_0(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.participant.is_dropout is False

    @staticmethod
    def vars_for_template(player: Player):
        parvars = player.participant.vars
        session = player.session

        return dict(
            par_vars=parvars,
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


class InsPilot_Q1(Page):
    form_model = "player"
    form_fields = ['compqns_payment_det']

    @staticmethod
    def is_displayed(player: Player):
        return player.session.config['instructionpilot']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        if timeout_happened:
            participant.is_dropout = True
            participant.dropout = "Dropped out at belief instructions page"
        else:
            participant.is_dropout = False

        participant.vars['compqns_payment_det'] = player.compqns_payment_det


class InsPilot_Q2(Page):
    form_model = "player"
    form_fields = ['compqns_optimal_belief0']

    @staticmethod
    def is_displayed(player: Player):
        return player.session.config['instructionpilot']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        if timeout_happened:
            participant.is_dropout = True
            participant.dropout = "Dropped out at belief instructions page"
        else:
            participant.is_dropout = False

        participant.vars['compqns_optimal_belief0'] = player.compqns_optimal_belief0


class InsPilot_Q3(Page):
    form_model = "player"
    form_fields = ['compqns_optimal_belief75']

    @staticmethod
    def is_displayed(player: Player):
        return player.session.config['instructionpilot']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        if timeout_happened:
            participant.is_dropout = True
            participant.dropout = "Dropped out at belief instructions page"
        else:
            participant.is_dropout = False

        participant.vars['compqns_optimal_belief75'] = player.compqns_optimal_belief75


class InsPilot_Q4(Page):
    form_model = "player"
    form_fields = ['compqns_payment_optimal']

    @staticmethod
    def is_displayed(player: Player):
        return player.session.config['instructionpilot']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        if timeout_happened:
            participant.is_dropout = True
            participant.dropout = "Dropped out at belief instructions page"
        else:
            participant.is_dropout = False

        participant.vars['compqns_payment_optimal'] = player.compqns_payment_optimal


page_sequence = [Instructions_Video_1]
