import random
import os
from definitions.distribution_types import getDelay
from datetime import datetime


def runSimulation(PetriNet, simLength: int, randomSeed: int = 1337, verbose: int = 1,  defTimeUnit: str = 'sec', logPath: str = './logs'):

    filePath = logPath + '/' + PetriNet.name + '/'
    makePetriNetFile(PetriNet, filePath)

    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d-%H-%M-%S-%f")

    filename = (
        filePath + 'sim_results/' + PetriNet.name + '_Simulation' + dt_string + '.txt')
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        print(PetriNet.name + ' simulation results\n', file=f)

    random.seed(randomSeed)  # TODO: change seeding for each experiment

    globalTimer = 0.0

    FEL = []

    while globalTimer <= simLength:

        # log simulation events
        with open(filename, 'a') as f:
            print('Simulation time: ' + str(globalTimer), file=f)

        # loop through all transitions and check if firing is enabled
        enabledTransitions = []
        enabledTimedTrans = []
        enabledImmediateTrans = []

        enabledTimedTrans, FEL = checkEnabledTimedTrans(
            PetriNet, globalTimer, FEL)
        enabledImmediateTrans = checkEnabledImmediateTrans(PetriNet)

        enabledTransitions = enabledTimedTrans + enabledImmediateTrans

        # make a list of enabled transitions, randomize their order and process them one by one (update, with checkEnabled() after every event)

        with open(filename, 'a') as f:
            print('\tExecuted events:', file=f)
            if(len(enabledTransitions) == 0):
                print('\tNone', file=f)

        eventCounter = 0

        while len(enabledTransitions) > 0:

            random.shuffle(enabledTransitions)  # TODO: not needed?

            randomEvent = random.choice(enabledTransitions)

            # process and log event
            eventCounter += 1
            processEvent(eventCounter, randomEvent, filename, FEL)

            enabledTransitions.clear()
            enabledTimedTrans.clear()
            enabledImmediateTrans.clear()

            enabledTimedTrans, FEL = checkEnabledTimedTrans(
                PetriNet, globalTimer, FEL)
            enabledImmediateTrans = checkEnabledImmediateTrans(PetriNet)
            enabledTransitions = enabledTimedTrans + enabledImmediateTrans

            FELstring = '\t' + 'Future Event List: '
            for event in FEL:
                FELstring += '(' + str(event[0].name) + \
                    ', ' + str(event[1]) + '), '
            FELstring += '\n'
            writeSimulationFile(FELstring, filename)

        # log current state of Petri Net (after processed events)

        # generate random delay based on distribution type for all ENABLED Timed Transitions
        # generateDelay(enabledTimedTrans)  # TODO: implement

        # increase global timer to reach the next firing
        #globalTimer += 1
        globalTimer = increaseGlobalTimer(FEL)


def checkEnabledImmediateTrans(PetriNet):

    enabledImmediateTransList = []

    for immediateTrans in PetriNet.immediateTransList:

        # default: enable all transitions, disable and iterate if does not meet requirements
        immediateTrans.enabled = True

        # check for guard value
        if(immediateTrans.guard is not None):
            if(eval(immediateTrans.guard) == False):
                immediateTrans.enabled = False
                continue

        # check for inhibitor arcs blocking
        if(len(immediateTrans.inhibArcs) > 0):
            jump = False
            for inhib in immediateTrans.inhibArcs:
                if(inhib.origin.tokens >= inhib.multiplicity):
                    immediateTrans.enabled = False
                    jump = True
                    break
            if(jump):
                continue

        # check for input arcs
        if(len(immediateTrans.inputArcs) > 0):
            jump = False
            for input in immediateTrans.inputArcs:
                if(input.fromPlace.tokens < input.multiplicity):
                    immediateTrans.enabled = False
                    jump = True
                    break
            if(jump):
                continue

        enabledImmediateTransList.append(immediateTrans)

    return enabledImmediateTransList


def checkEnabledTimedTrans(PetriNet, simulationTime, FEL):

    enabledTimedTransList = []

    for timedTrans in PetriNet.timedTransList:

        # default: enable all transitions, disable and iterate if does not meet requirements
        timedTrans.enabled = True

        # check for guard value
        if(timedTrans.guard is not None):
            if(eval(timedTrans.guard) == False):
                timedTrans.enabled = False
                timedTrans.delay = None
                continue

        # check for inhibitor arcs blocking
        if(len(timedTrans.inhibArcs) > 0):
            jump = False
            for inhib in timedTrans.inhibArcs:
                if(inhib.origin.tokens >= inhib.multiplicity):
                    timedTrans.enabled = False
                    timedTrans.delay = None
                    jump = True
                    break
            if(jump):
                continue

        # check for input arcs
        if(len(timedTrans.inputArcs) > 0):
            jump = False
            for input in timedTrans.inputArcs:
                if(input.fromPlace.tokens < input.multiplicity):
                    timedTrans.enabled = False
                    timedTrans.delay = None
                    jump = True
                    break
            if(jump):
                continue

        # firing is enabled, generate delay for timed transition
        if(timedTrans.delay is None):
            delay = generateDelay(timedTrans, simulationTime)
            FEL.append((timedTrans, delay))
            FEL.sort(key=sortDelay)
            continue

        # check if firing delay has elapsed
        if(timedTrans.delay != simulationTime):
            timedTrans.enabled = False
            continue

        enabledTimedTransList.append(timedTrans)

    return enabledTimedTransList, FEL


def processEvent(eventNo, enabledTrans, filePath, FEL):

    # update statistics
    enabledTrans.fireCount += 1

    # building event info string for log
    eventString = (
        '\t' + str(eventNo) + '. event: ' + enabledTrans.name + ' ')
    if(enabledTrans.__class__.__name__ == 'TimedTransition'):
        eventString += 'timed transition '
    elif(enabledTrans.__class__.__name__ == 'ImmediateTransition'):
        eventString += 'immediate transition '
    eventString += 'fired, '

    # remove tokens from input places according to arc multiplicity
    if(len(enabledTrans.inputArcs) > 0):
        for input in enabledTrans.inputArcs:
            input.fromPlace.tokens -= input.multiplicity

            eventString += str(input.multiplicity) + \
                ' tokens removed from Place ' + input.fromPlace.name + ', '

    # add tokens to output places according to arc multiplicity
    # update Place token statistics
    if(len(enabledTrans.outputArcs) > 0):
        for output in enabledTrans.outputArcs:
            output.toPlace.tokens += output.multiplicity
            output.toPlace.totalTokens += output.multiplicity
            if(output.toPlace.tokens > output.toPlace.maxTokens):
                output.toPlace.maxTokens = output.toPlace.tokens

            eventString += str(output.multiplicity) + \
                ' tokens added to Place ' + output.toPlace.name + ', '

    writeSimulationFile(eventString, filePath)

    # reset timer for timed transition, remove from FEL
    if(enabledTrans.__class__.__name__ == 'TimedTransition'):
        FEL.remove((enabledTrans, enabledTrans.delay))
        FEL.sort(key=sortDelay)
        enabledTrans.delay = None


def generateDelay(trans, simulationTime):

    trans.delay = getDelay(trans.distType, trans.a,
                           trans.b, trans.c, trans.d) + simulationTime
    return trans.delay


def makePetriNetFile(PetriNet, filePath):

    filename = filePath + PetriNet.name + '_PetriNet.pnml'
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, 'w') as f:
        print("Places:\n", file=f)
        print(PetriNet.getPlaces(), file=f)
        print("Timed Transitions:\n", file=f)
        print(PetriNet.getTimedTransitions(), file=f)
        print("Immediate Transitions:\n", file=f)
        print(PetriNet.getImmediateTransitions(), file=f)
        print("Input Arcs:\n", file=f)
        print(PetriNet.getInputArcs(), file=f)
        print("Output Arcs:\n", file=f)
        print(PetriNet.getOutputArcs(), file=f)
        print("Inhibitor Arcs:\n", file=f)
        print(PetriNet.getInhibArcs(), file=f)


def writeSimulationFile(eventText, filePath):

    with open(filePath, 'a') as f:
        print(eventText, file=f)


def sortDelay(tuple):
    return tuple[1]


def increaseGlobalTimer(FEL):
    return FEL[0][1]
