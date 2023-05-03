import random
import os
import numpy as np
from definitions.distribution_types import getDelay
from definitions.timeunit_types import TimeUnitType, getTimeMultiplier
from datetime import datetime


def simulation(PetriNet, simLength, simSeed, verbose: int,  defTimeUnit: TimeUnitType, conditionals, logPath: str):

    # TODO: make typecheck for Petri Net param + other params!

    # set seed for current simulation run
    # generating random delays is done with scipy library, which uses the numpy library's random function
    np.random.seed(simSeed)

    # default time unit setting of simulation
    timeTypes = [member.name for member in TimeUnitType]

    if(defTimeUnit not in timeTypes):
        returnMsg = "The default time unit type set for simulation of Petri Net named: " + \
            PetriNet.name + " is not defined.\nSupported time unit types: "
        for member in TimeUnitType:
            returnMsg += '[' + member.name + \
                ": " + member.value + '], '
        raise Exception(
            returnMsg
        )

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
        svcString = 'Timestamp (' + defTimeUnit + ') / Place'
        for place in PetriNet.placeList:
            svcString += ';' + place.name
        print(svcString, file=f)

    # start global timer
    globalTimer = 0.0

    # set simulation step counter
    simStepCounter = 0

    # Future Event List, for logging purpose
    FEL = []

    # Petri Net Marking list, used to record statistics of different markings
    PNmarkings = []

    # Marking total time list, used to record statistics of time of different markings
    markings_time = []

    # counter for occurrence of different markings
    markings_count = []

    # temporary variables to store previous marking and timestamp
    prevMarking = ''
    prevTS = 0.0

    # counter for occurrence of conditionals
    cond_count = []
    if(conditionals is not None):
        for cond in conditionals:
            cond_count.append(0)

    # Conditions total time list, used to record statistics of time of conditionals
    cond_time = []
    if(conditionals is not None):
        for cond in conditionals:
            cond_time.append(0.0)

    # list of previous state of conditionals
    cond_prevVal = []
    if(conditionals is not None):
        for cond in conditionals:
            cond_prevVal.append(False)

    # discover and store references & probabilities for competing immediate transitions
    competitiveTransList, competitiveProbabilities = checkCompetitiveTransitions(
        PetriNet)

    # iterate until simulation (global) timer does NOT reach defined time length
    # TODO: make last iteration for last timestamp? (won't be changes compared to last iteration due to simulation execution logic)
    while globalTimer <= simLength:

        # start text file logging
        with open(filename_txt, 'a') as f:
            print('Simulation time: ' + str(globalTimer) +
                  ' ' + defTimeUnit, file=f)
            printToTerminal('Simulation time: ' +
                            str(globalTimer) + ' ' + defTimeUnit, verbose)
            simStepCounter += 1
            print('Simulation step: ' + str(simStepCounter), file=f)
            printToTerminal('Simulation step: ' + str(simStepCounter), verbose)

        # lists to store enabled transitions to choose from at each simulation step (overwritten after every execution)
        enabledTransitions = []
        enabledTimedTrans = []
        enabledImmediateTrans = []

        # separate list to store enabled competing events to choose from at each simulation step (overwritten after every execution)
        enabledCompetingTransitions = []

        enabledTimedTrans, FEL = checkEnabledTimedTrans(
            PetriNet, globalTimer, FEL, defTimeUnit)

        enabledImmediateTrans = checkEnabledImmediateTrans(PetriNet)

        enabledCompetingTransitions = checkEnabledCompetingImmediateTrans(
            competitiveTransList, competitiveProbabilities)

        enabledTransitions = enabledTimedTrans + \
            enabledImmediateTrans + enabledCompetingTransitions

        # log executed events (if applicable) to text file
        with open(filename_txt, 'a') as f:
            print('\tExecuted events:', file=f)
            printToTerminal('Executed events:', verbose)
            if(len(enabledTransitions) == 0):
                print('\tNone\n', file=f)
                printToTerminal('\tNone', verbose)

        # counter to count number of executed events per simulation step
        eventCounter = 0

        # choose a random event from list of enabled events, execute it, refresh event list, repeat until no enabled events remain
        while len(enabledTransitions) > 0:

            # choose random event with random.choice()
            randomEvent = random.choice(enabledTransitions)

            # increase event counter
            eventCounter += 1

            # execute event and update text log file
            processEvent(eventCounter, randomEvent, filename_txt, FEL, verbose)

            # clear enabled transition lists
            enabledTransitions.clear()
            enabledTimedTrans.clear()
            enabledImmediateTrans.clear()
            enabledCompetingTransitions.clear()

            # update enabled transition lists
            enabledTimedTrans, FEL = checkEnabledTimedTrans(
                PetriNet, globalTimer, FEL, defTimeUnit)
            enabledImmediateTrans = checkEnabledImmediateTrans(PetriNet)
            enabledCompetingTransitions = checkEnabledCompetingImmediateTrans(
                competitiveTransList, competitiveProbabilities)
            enabledTransitions = enabledTimedTrans + \
                enabledImmediateTrans + enabledCompetingTransitions

        # log FEL to text file
        FELstring = '\n\t' + 'Future Event List: '
        if(len(FEL) > 0):
            for event in FEL:
                FELstring += '(' + str(event[0].name) + \
                    ', ' + str(event[1]) + '), '
        else:
            FELstring += 'None'
        FELstring += '\n'
        writeSimulationFile(FELstring, filename_txt, verbose)

        # log current state of Petri Net (changes after processed events): number of tokens at places, number of firings at transitions
        # record current state of Petri Net to logging variables and list
        currentStateString = "\tCurrent marking of Petri Net (changes):\n"
        svcString = str(globalTimer)
        first = True
        currentMarking = '('

        for place in PetriNet.placeList:
            svcString += ';' + str(place.tokens)
            if first:
                currentMarking += str(place.tokens)
                first = False
            else:
                currentMarking += ', ' + str(place.tokens)
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
        currentStateString += '\n\tStatistics (changes):\n'
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

        currentMarking += ')'

        if(currentMarking not in PNmarkings):
            PNmarkings.append(currentMarking)
            markings_time.append(0.0)
            markings_count.append(1)
        else:
            markings_count[PNmarkings.index(currentMarking)] += 1

        if(prevMarking in PNmarkings):
            markings_time[PNmarkings.index(
                prevMarking)] += (globalTimer - prevTS)

        currentStateString += '\n\tOccurred markings, nbr. of occurrence, total time spent in marking, and percentage of time spent in marking:\n'

        for id, mark in enumerate(PNmarkings):
            currentStateString += '\t' + mark + ': ' + str(markings_count[id]) + ', ' + str(
                markings_time[id]) + ', '
            if(globalTimer == 0.0):
                currentStateString += 'N/A\n'
            else:
                currentStateString += str(markings_time[id]/globalTimer) + '\n'

        # if additional conditions were defined, check if they're satisfied by the current marking and create log
        currentStateString += '\n\tAdditional conditions, current value, nbr. of occurrence, ratio of occurrence / nbr. of states, total time spent while true, and percentage of time spent while true:\n'
        if(conditionals is None):
            currentStateString += '\t\tNone\n'
        else:
            for id, cond in enumerate(conditionals):
                currentStateString += '\t\t' + str(cond[0]) + ': '
                cond_fail = False
                for func_nbr in range(0, (len(cond) - 1)):
                    if(not cond[func_nbr+1]()):
                        cond_fail = True
                        break
                if(cond_prevVal[id]):
                    cond_time[id] += globalTimer - prevTS
                if(cond_fail):
                    cond_prevVal[id] = False
                    currentStateString += 'False, '
                else:
                    cond_count[id] += 1
                    cond_prevVal[id] = True
                    currentStateString += 'True, '
                currentStateString += str(cond_count[id]) + ', ' + str(
                    cond_count[id]) + ' / ' + str(simStepCounter) + ' (=' + str(cond_count[id]/simStepCounter) + ')' +\
                    ', ' + str(cond_time[id]) + ', '
                if(globalTimer == 0.0):
                    currentStateString += 'N/A\n'
                else:
                    currentStateString += str(cond_time[id]/globalTimer) + '\n'

        writeSimulationFile(currentStateString, filename_txt, verbose)

        # log current marking to csv file
        with open(filename_csv, 'a') as f:
            print(svcString, file=f)

        # update variables used to track previous step in simulation
        prevMarking = currentMarking
        prevTS = globalTimer

        # advance global timer to reach the next firing
        # simulation end time reached, stop simulation
        if(globalTimer == simLength):
            writeSimulationFile('Simulation ended at: ' +
                                str(simLength) + ' ' + defTimeUnit, filename_txt, verbose)
            break
        # no more events in FEL: simulation ended before reaching the defined length, end simulation at defined length
        if(len(FEL) == 0):
            globalTimer = simLength
        else:
            # timestamp of next event in FEL exceeds simulation length, end simulation at defined length
            if(increaseGlobalTimer(FEL) > simLength):
                globalTimer = simLength
            else:
                # advance to timestamp of next event in FEL
                globalTimer = increaseGlobalTimer(FEL)


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


def checkEnabledTimedTrans(PetriNet, simulationTime, FEL, simTimeUnit):

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
            delay = generateDelay(timedTrans, simulationTime, simTimeUnit)
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


def processEvent(eventNo, enabledTrans, filePath, FEL, verbose):

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

    writeSimulationFile(eventString, filePath, verbose)

    # reset timer for timed transition, remove from FEL
    if(enabledTrans.__class__.__name__ == 'TimedTransition'):
        FEL.remove((enabledTrans, enabledTrans.delay))
        FEL.sort(key=sortDelay)
        enabledTrans.delay = None


def generateDelay(trans, simulationTime, simTimeUnit):

    trans.delay = (getDelay(trans.distType, trans.a,
                            trans.b, trans.c, trans.d) * getTimeMultiplier(simTimeUnit, trans.timeUnitType)) + simulationTime

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


def writeSimulationFile(eventText, filePath, verbose):

    printToTerminal(eventText, verbose)
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


def printToTerminal(text, verbose):
    if(verbose > 0):
        print(text)
