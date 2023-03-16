import random


def runSimulation(PetriNet, verbose: int = 1,  defTimeUnit: str = sec):

    globalTimer = 0

    # loop through all transitions and check if firing is enabled
    enabledTransitions = []

    enabledTransitions = checkEnabled(PetriNet)

    random.shuffle(enabledTransitions)  # not needed?

    randomEvent = random.choice(enabledTransitions)

    # generate random delay based on distribution type for all ENABLED Timed Transitions
    generateDelay()  # TODO: implement

    # make a list of enabled transitions, randomize their order and process them one by one (update, with checkEnabled() after every event)

    while len(enabledTransitions) > 0:

        processEvent(randomEvent)

        enabledTransitions.clear()

        enabledTransitions = checkEnabled(PetriNet)

        random.shuffle(enabledTransitions)  # not needed?

        randomEvent = random.choice(enabledTransitions)

    # increase global timer to reach the next firing
    increaseGlobalTimer()


def checkEnabled(PetriNet):

    enabledTransList = []

    for timedTrans in PetriNet.timedTransList:

        # default: enable all transitions, disable and iterate if does not meet requirements
        timedTrans.enabled = True

        # check for guard value
        if(eval(timedTrans.guard) == False):
            timedTrans.enabled = False
            continue

        # check for inhibitor arcs blocking
        jump = False
        for inhib in timedTrans.inhibArcs:
            if(inhib.origin.tokens >= inhib.multiplicity):
                timedTrans.enabled = False
                jump = True
                break
        if(jump):
            continue

        # check for input arcs
        jump = False
        for input in timedTrans.inputArcs:
            if(input.fromPlace.tokens < input.multiplicity):
                timedTrans.enabled = False
                jump = True
                break
        if(jump):
            continue

        enabledTransList.append(timedTrans)

    for immediateTrans in PetriNet.immediateTransList:

        # default: enable all transitions, disable and iterate if does not meet requirements
        immediateTrans.enabled = True

        # check for guard value
        if(eval(immediateTrans.guard) == False):
            immediateTrans.enabled = False
            continue

        # check for inhibitor arcs blocking
        jump = False
        for inhib in immediateTrans.inhibArcs:
            if(inhib.origin.tokens >= inhib.multiplicity):
                immediateTrans.enabled = False
                jump = True
                break
        if(jump):
            continue

        # check for input arcs
        jump = False
        for input in immediateTrans.inputArcs:
            if(input.fromPlace.tokens < input.multiplicity):
                immediateTrans.enabled = False
                jump = True
                break
        if(jump):
            continue

        enabledTransList.append(immediateTrans)

    return enabledTransList


def processEvent(enabledTrans):

    # remove tokens from input places according to arc multiplicity
    for input in enabledTrans.inputArcs:
        input.fromPlace.tokens -= input.multiplicity

    # add tokens to output places according to arc multiplicity
    for output in enabledTrans.outputArcs:
        output.toPlace.tokens += output.multiplicity

    # TODO: reset timer for timed transition


def generateDelay(timedTrans):
