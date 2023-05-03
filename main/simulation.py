import random
import os
import numpy as np
from definitions.distribution_types import getDelay
from definitions.timeunit_types import TimeUnitType, getTimeMultiplier
from .generateLogs import generateLogFile


def simulation(PetriNet, simLength, simSeed, verbose: int,  defTimeUnit: TimeUnitType, conditionals, filePath: str, simCount: int):

    # set seed for current simulation run
    # generating random delays is done with scipy library, which uses the numpy library's random function
    np.random.seed(simSeed)
    random.seed(simSeed)

    # create simulation files (text log & csv)
    filename_txt = (
        filePath + PetriNet.name + '_SimulationRun_' + str(simCount) + '.txt')
    filename_csv = (
        filePath + PetriNet.name + '_SimulationRun_' + str(simCount) + '.csv')

    # start simulation text log
    generateLogFile('\n' + PetriNet.name + ' ' + str(simCount) +
                    '. simulation run results', filename_txt, verbose, True)

    # start simulation csv log
    csvString = PetriNet.name + ' ' + \
        str(simCount) + '. simulation run results\n\nTimestamp (' + \
        defTimeUnit + ') / Place'
    for place in PetriNet.placeList:
        csvString += ';' + place.name
    generateLogFile(csvString, filename_csv, 0)

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

    # iterate until simulation (global) timer reaches defined time length, repeat for ending timestamp
    while globalTimer <= simLength:

        simStepCounter += 1

        # start text file logging
        generateLogFile('\nSimulation time: ' + str(globalTimer) +
                        ' ' + defTimeUnit + '\nSimulation step: ' + str(simStepCounter), filename_txt, verbose, True)

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
        logText = '\n\tExecuted events:'
        if(len(enabledTransitions) == 0):
            logText += '\n\t\tNone'

        generateLogFile(logText, filename_txt, verbose, True)

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
        FELstring = '\n\t' + 'Future Event List:\n\t\t'
        if(len(FEL) > 0):
            for id, event in enumerate(FEL):
                FELstring += '(' + str(event[0].name) + \
                    ', ' + str(event[1]) + ' ' + defTimeUnit + ')'
                if(not id == (len(FEL)-1)):
                    FELstring += ', '
        else:
            FELstring += 'None'
        generateLogFile(FELstring, filename_txt, verbose, True)

        # log current state of Petri Net (changes after processed events): number of tokens at places, number of firings at transitions
        # record current state of Petri Net to logging variables and list
        currentStateString = "\n\tCurrent marking of Petri Net (changes):\n"
        csvString = str(globalTimer)
        first = True
        currentMarking = '('

        for place in PetriNet.placeList:
            csvString += ';' + str(place.tokens)
            if first:
                currentMarking += str(place.tokens)
                first = False
            else:
                currentMarking += ', ' + str(place.tokens)
            currentStateString += "\t\t" + place.name + \
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
            currentStateString += "\t\t" + trans.name + \
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
            currentStateString += "\t\t" + trans.name + \
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

        currentStateString += '\n\tOccurred markings, nbr. of occurrence, total time spent in marking, and ratio of time spent in marking (percentage):\n'

        for id, mark in enumerate(PNmarkings):
            currentStateString += '\t\t' + mark + ': ' + str(markings_count[id]) + ', ' + str(
                markings_time[id]) + ' ' + defTimeUnit + ', '
            if(globalTimer == 0.0):
                currentStateString += 'N/A\n'
            else:
                ratio = markings_time[id]/globalTimer
                currentStateString += str(ratio) + \
                    ' (' + str(ratio * 100) + '%)\n'

        # if additional conditions were defined, check if they're satisfied by the current marking and create log
        currentStateString += '\n\tAdditional conditions, current value, nbr. of occurrence, ratio of occurrence / nbr. of states, total time spent while true, and ratio of time spent while true (percentage):\n'
        if(conditionals is None):
            currentStateString += '\t\tNone'
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
                    ', ' + str(cond_time[id]) + ' ' + defTimeUnit + ', '
                if(globalTimer == 0.0):
                    currentStateString += 'N/A\n'
                else:
                    ratio = cond_time[id]/globalTimer
                    currentStateString += str(ratio) + \
                        ' (' + str(ratio * 100) + '%)\n'

        generateLogFile(currentStateString, filename_txt, verbose, True)

        # log current marking to csv file
        generateLogFile(csvString, filename_csv, 0)

        # update variables used to track previous step in simulation
        prevMarking = currentMarking
        prevTS = globalTimer

        # advance global timer to reach the next firing
        # simulation end time reached, stop simulation
        if(globalTimer == simLength):
            generateLogFile(
                '\nSimulation ended at: ' + str(simLength) + ' ' + defTimeUnit, filename_txt, verbose, True)
            break
        # no more events in FEL: simulation ended before reaching the defined length, end simulation at defined length
        if(len(FEL) == 0):
            globalTimer = simLength
        else:
            # timestamp of next event in FEL exceeds simulation length, end simulation at defined length
            if(FEL[0][1] > simLength):
                globalTimer = simLength
            else:
                # advance to timestamp of next event in FEL
                globalTimer = FEL[0][1]


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
        '\t\t' + str(eventNo) + '. event: ' + enabledTrans.name + ' ')
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

    generateLogFile(eventString, filePath, verbose, True)

    # reset timer for timed transition, remove from FEL
    if(enabledTrans.__class__.__name__ == 'TimedTransition'):
        FEL.remove((enabledTrans, enabledTrans.delay))
        FEL.sort(key=sortDelay)
        enabledTrans.delay = None


def generateDelay(trans, simulationTime, simTimeUnit):

    trans.delay = (getDelay(trans.distType, trans.a,
                            trans.b, trans.c, trans.d) * getTimeMultiplier(simTimeUnit, trans.timeUnitType)) + simulationTime

    return trans.delay


def sortDelay(tuple):
    return tuple[1]


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
