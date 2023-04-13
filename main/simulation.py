import random
import os
from definitions.distribution_types import getDelay
from datetime import datetime


def simulation(PetriNet, simLength: int, randomSeed: int = 1337, verbose: int = 1,  defTimeUnit: str = 'sec', logPath: str = './logs'):

    # create folder structure (default: root/logs/)
    filePath = logPath + '/' + PetriNet.name + '/'

    # create .pnml file of Petri Net
    # TODO:
    makePetriNetFile(PetriNet, filePath)

    # create simulation file (text log & csv), unique by adding current timestamp to filename
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d-%H-%M-%S-%f")

    filename_txt = (
        filePath + 'sim_results/' + PetriNet.name + '_Simulation' + dt_string + '.txt')
    filename_csv = (
        filePath + 'sim_results/' + PetriNet.name + '_Simulation' + dt_string + '.csv')
    os.makedirs(os.path.dirname(filename_txt), exist_ok=True)
    os.makedirs(os.path.dirname(filename_csv), exist_ok=True)
    with open(filename_txt, 'w') as f:
        print(PetriNet.name + ' simulation results\n', file=f)
    with open(filename_csv, 'w') as f:
        print(PetriNet.name + ' simulation results\n', file=f)
        svcString = 'Timestamp / Place'
        for place in PetriNet.placeList:
            svcString += ';' + place.name
        print(svcString, file=f)

    # set seed for random number generation
    # TODO: change for each random() lib call?
    random.seed(randomSeed)

    # start global timer
    globalTimer = 0.0

    # Future Event List, for logging purpose
    FEL = []

    # discover and store references & probabilities for competing immediate transitions
    competitiveTransList, competitiveProbabilities = checkCompetitiveTransitions(
        PetriNet)

    # iterate until simulation (global) timer does NOT reach defined time length
    # TODO: make last iteration for last timestamp? (won't be changes compared to last iteration due to simulation execution logic)
    while globalTimer <= simLength:

        # start text file logging
        with open(filename_txt, 'a') as f:
            print('Simulation time: ' + str(globalTimer), file=f)

        # lists to store enabled transitions to choose from at each simulation step (overwritten after every execution)
        enabledTransitions = []
        enabledTimedTrans = []
        enabledImmediateTrans = []

        # separate list to store enabled competing events to choose from at each simulation step (overwritten after every execution)
        enabledCompetingTransitions = []

        enabledTimedTrans, FEL = checkEnabledTimedTrans(
            PetriNet, globalTimer, FEL)

        enabledImmediateTrans = checkEnabledImmediateTrans(PetriNet)

        enabledCompetingTransitions = checkEnabledCompetingImmediateTrans(
            competitiveTransList, competitiveProbabilities)

        enabledTransitions = enabledTimedTrans + \
            enabledImmediateTrans + enabledCompetingTransitions

        # log executed events (if applicable) to text file
        with open(filename_txt, 'a') as f:
            print('\tExecuted events:', file=f)
            if(len(enabledTransitions) == 0):
                print('\tNone\n', file=f)

        # counter to count number of executed events per simulation step
        eventCounter = 0

        # choose a random event from list of enabled events, execute it, refresh event list, repeat until no enabled events remain
        while len(enabledTransitions) > 0:

            # TODO: not needed?
            random.shuffle(enabledTransitions)

            # choose random event with random.choice()
            randomEvent = random.choice(enabledTransitions)

            # increase event counter
            eventCounter += 1

            # execute event and update text log file
            processEvent(eventCounter, randomEvent, filename_txt, FEL)

            # clear enabled transition lists
            enabledTransitions.clear()
            enabledTimedTrans.clear()
            enabledImmediateTrans.clear()
            enabledCompetingTransitions.clear()

            # update enabled transition lists
            enabledTimedTrans, FEL = checkEnabledTimedTrans(
                PetriNet, globalTimer, FEL)
            enabledImmediateTrans = checkEnabledImmediateTrans(PetriNet)
            enabledCompetingTransitions = checkEnabledCompetingImmediateTrans(
                competitiveTransList, competitiveProbabilities)
            enabledTransitions = enabledTimedTrans + \
                enabledImmediateTrans + enabledCompetingTransitions

        # log FEL to text file
        FELstring = '\t' + 'Future Event List: '
        if(len(FEL) > 0):
            for event in FEL:
                FELstring += '(' + str(event[0].name) + \
                    ', ' + str(event[1]) + '), '
        else:
            FELstring += 'None'
        FELstring += '\n'
        writeSimulationFile(FELstring, filename_txt)

        # log current state of Petri Net (changes after processed events): number of tokens at places, number of firings at transitions
        currentStateString = "\tCurrent state of Petri Net (changes):\n"
        for place in PetriNet.placeList:
            currentStateString += "\t" + place.name + \
                " tokens: " + str(place.tokens)
            if place.prevTokens > place.tokens:
                currentStateString += ' (change: ' + \
                    str(place.tokens - place.prevTokens) + ')'
                place.prevTokens = place.tokens
            elif place.prevTokens < place.tokens:
                currentStateString += ' (change: +' + \
                    str(place.tokens - place.prevTokens) + ')'
                place.prevTokens = place.tokens
            currentStateString += '\n'
        for trans in PetriNet.timedTransList:
            currentStateString += "\t" + trans.name + \
                " firings: " + str(trans.fireCount)
            if trans.prevFireCount > trans.fireCount:
                currentStateString += ' (change: ' + \
                    str(trans.fireCount - trans.prevFireCount) + ')'
                trans.prevFireCount = trans.fireCount
            elif trans.prevFireCount < trans.fireCount:
                currentStateString += ' (change: +' + \
                    str(trans.fireCount - trans.prevFireCount) + ')'
                trans.prevFireCount = trans.fireCount
            currentStateString += '\n'
        for trans in PetriNet.immediateTransList:
            currentStateString += "\t" + trans.name + \
                " firings: " + str(trans.fireCount)
            if trans.prevFireCount > trans.fireCount:
                currentStateString += ' (change: ' + \
                    str(trans.fireCount - trans.prevFireCount) + ')'
                trans.prevFireCount = trans.fireCount
            elif trans.prevFireCount < trans.fireCount:
                currentStateString += ' (change: +' + \
                    str(trans.fireCount - trans.prevFireCount) + ')'
                trans.prevFireCount = trans.fireCount
            currentStateString += '\n'
        writeSimulationFile(currentStateString, filename_txt)

        # log current marking to csv file
        with open(filename_csv, 'a') as f:
            svcString = str(globalTimer)
            for place in PetriNet.placeList:
                svcString += ';' + str(place.tokens)
            print(svcString, file=f)

        # advance global timer to reach the next firing
        if(len(FEL) != 0):
            globalTimer = increaseGlobalTimer(FEL)
        else:
            writeSimulationFile('Simulation ended at: ' +
                                str(globalTimer), filename_txt)
            break


def checkEnabledImmediateTrans(PetriNet):

    enabledImmediateTransList = []

    for immediateTrans in PetriNet.immediateTransList:

        # skip competing immediate transitions, they are checked in separate function
        if (immediateTrans.competing):
            continue

        # default: enable all transitions, disable and iterate if does not meet requirements
        immediateTrans.enabled = True

        # check for guard value
        if(immediateTrans.guard is not None):
            if(immediateTrans.guard() == False):
                immediateTrans.enabled = False
                continue

        # check for inhibitor arcs blocking
        if(len(immediateTrans.inhibArcs) > 0):
            jump = False
            for inhib in immediateTrans.inhibArcs:
                if(checkType(inhib.multiplicity) == 'int'):
                    if(inhib.origin.tokens >= inhib.multiplicity):
                        immediateTrans.enabled = False
                        jump = True
                        break
                else:
                    if(inhib.origin.tokens >= inhib.multiplicity()):
                        immediateTrans.enabled = False
                        jump = True
                        break
            if(jump):
                continue

        # check for input arcs
        if(len(immediateTrans.inputArcs) > 0):
            jump = False
            for input in immediateTrans.inputArcs:
                if(checkType(input.multiplicity) == 'int'):
                    if(input.fromPlace.tokens < input.multiplicity):
                        immediateTrans.enabled = False
                        jump = True
                        break
                else:
                    if(input.fromPlace.tokens < input.multiplicity()):
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
            if(timedTrans.guard() == False):
                timedTrans.enabled = False
                if(timedTrans.agePolicy == 'R_ENABLE'):
                    timedTrans.delay = None
                if (FEL.count((timedTrans, timedTrans.delay)) > 0):
                    FEL.remove((timedTrans, timedTrans.delay))
                continue

        # check for inhibitor arcs blocking
        if(len(timedTrans.inhibArcs) > 0):
            jump = False
            for inhib in timedTrans.inhibArcs:
                if(checkType(inhib.multiplicity) == 'int'):
                    if(inhib.origin.tokens >= inhib.multiplicity):
                        timedTrans.enabled = False
                        if(timedTrans.agePolicy == 'R_ENABLE'):
                            timedTrans.delay = None
                        if (FEL.count((timedTrans, timedTrans.delay)) > 0):
                            FEL.remove((timedTrans, timedTrans.delay))
                        jump = True
                        break
                else:
                    if(inhib.origin.tokens >= inhib.multiplicity()):
                        timedTrans.enabled = False
                        if(timedTrans.agePolicy == 'R_ENABLE'):
                            timedTrans.delay = None
                        if (FEL.count((timedTrans, timedTrans.delay)) > 0):
                            FEL.remove((timedTrans, timedTrans.delay))
                        jump = True
                        break
            if(jump):
                continue

        # check for input arcs
        if(len(timedTrans.inputArcs) > 0):
            jump = False
            for input in timedTrans.inputArcs:
                if(checkType(input.multiplicity) == 'int'):
                    if(input.fromPlace.tokens < input.multiplicity):
                        timedTrans.enabled = False
                        if(timedTrans.agePolicy == 'R_ENABLE'):
                            timedTrans.delay = None
                        if (FEL.count((timedTrans, timedTrans.delay)) > 0):
                            FEL.remove((timedTrans, timedTrans.delay))
                        jump = True
                        break
                else:
                    if(input.fromPlace.tokens < input.multiplicity()):
                        timedTrans.enabled = False
                        if(timedTrans.agePolicy == 'R_ENABLE'):
                            timedTrans.delay = None
                        if (FEL.count((timedTrans, timedTrans.delay)) > 0):
                            FEL.remove((timedTrans, timedTrans.delay))
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

        # re-enabled timed transition with race age policy
        if(timedTrans.agePolicy == 'R_AGE'):
            if (FEL.count((timedTrans, timedTrans.delay)) == 0):
                FEL.append((timedTrans, timedTrans.delay))
                FEL.sort(key=sortDelay)

        # check if firing delay has elapsed
        if(timedTrans.delay > simulationTime):
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
            if(checkType(input.multiplicity) == 'int'):
                input.fromPlace.tokens -= input.multiplicity
                eventString += str(input.multiplicity)
            else:
                input.fromPlace.tokens -= input.multiplicity()
                eventString += str(input.multiplicity())

            eventString += ' tokens removed from Place ' + input.fromPlace.name + ', '

    # add tokens to output places according to arc multiplicity
    # update Place token statistics
    if(len(enabledTrans.outputArcs) > 0):
        for output in enabledTrans.outputArcs:
            if(checkType(output.multiplicity) == 'int'):
                output.toPlace.tokens += output.multiplicity
                output.toPlace.totalTokens += output.multiplicity
                eventString += str(output.multiplicity)
            else:
                output.toPlace.tokens += output.multiplicity()
                output.toPlace.totalTokens += output.multiplicity()
                eventString += str(output.multiplicity())
            if(output.toPlace.tokens > output.toPlace.maxTokens):
                output.toPlace.maxTokens = output.toPlace.tokens

            eventString += ' tokens added to Place ' + output.toPlace.name + ', '

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


def checkCompetitiveTransitions(PetriNet):

    competitiveTransList = []
    competitiveProbabilities = []

    for place in PetriNet.placeList:
        transTuple = ()
        probTuple = ()
        for arc in place.inputArcs:
            if checkType(arc.toTrans) == 'ImmediateTransition':
                if arc.toTrans.fireProbability != 1.0:
                    arc.toTrans.competing = True  # not need?
                    transTuple = transTuple + (arc.toTrans,)
                    probTuple = probTuple + (arc.toTrans.fireProbability,)
        if len(transTuple) > 1:
            competitiveTransList.append(transTuple)
            competitiveProbabilities.append(probTuple)

    return competitiveTransList, competitiveProbabilities


def checkType(object):
    return object.__class__.__name__


def checkEnabledCompetingImmediateTrans(transList, probList):

    enabledChoices = []

    for id, choices in enumerate(transList):

        disableChoice = False

        for option in choices:

            # safety check if competing event was discovered and registered during PN initialization
            # TODO: redundant, remove?
            if (not option.competing):
                disableChoice = True
                break

            # default: enable all transitions, disable and iterate if does not meet requirements
            option.enabled = True

            # check for guard value
            if(option.guard is not None):
                if(option.guard() == False):
                    option.enabled = False
                    disableChoice = True
                    break

            # check for inhibitor arcs blocking
            if(len(option.inhibArcs) > 0):
                jump = False
                for inhib in option.inhibArcs:
                    if(checkType(inhib.multiplicity) == 'int'):
                        if(inhib.origin.tokens >= inhib.multiplicity):
                            option.enabled = False
                            jump = True
                            break
                    else:
                        if(inhib.origin.tokens >= inhib.multiplicity()):
                            option.enabled = False
                            jump = True
                            break
                if(jump):
                    disableChoice = True
                    break

            # check for input arcs
            if(len(option.inputArcs) > 0):
                jump = False
                for input in option.inputArcs:
                    if(checkType(input.multiplicity) == 'int'):
                        if(input.fromPlace.tokens < input.multiplicity):
                            option.enabled = False
                            jump = True
                            break
                    else:
                        if(input.fromPlace.tokens < input.multiplicity()):
                            option.enabled = False
                            jump = True
                            break
                if(jump):
                    disableChoice = True
                    break

        if (disableChoice):
            continue
        choice = random.choices(choices, probList[id])
        enabledChoices = enabledChoices + choice

    return enabledChoices
