import os
import inspect


def generatePNDescription(PetriNet, fileName: str):

    # create folder and file for PetriNet (default: root/logs/...)
    os.makedirs(os.path.dirname(fileName), exist_ok=True)

    with open(fileName, 'w') as f:
        print("Places:", file=f)
        print('\t'.join(PetriNet.getPlaces().splitlines(True)), file=f)
        print("Timed Transitions:", file=f)
        print('\t'.join(PetriNet.getTimedTransitions().splitlines(True)), file=f)
        print("Immediate Transitions:", file=f)
        print('\t'.join(PetriNet.getImmediateTransitions().splitlines(True)), file=f)
        print("Input Arcs:", file=f)
        print('\t'.join(PetriNet.getInputArcs().splitlines(True)), file=f)
        print("Output Arcs:", file=f)
        print('\t'.join(PetriNet.getOutputArcs().splitlines(True)), file=f)
        print("Inhibitor Arcs:", file=f)
        print('\t'.join(PetriNet.getInhibArcs().splitlines(True)), file=f)


def generatePNML(petriNet, fileName: str):
    # pass

    # create folder and file for PetriNet (default: root/logs/...)
    os.makedirs(os.path.dirname(fileName), exist_ok=True)
    PNDict = {}

    with open(fileName, 'w') as f:
        print("<?xml version=\"1.0\" encoding=\"UTF-8\"?>", file=f)
        print("<pnml xmlns=\"https://www.pnml.org/version-2009/version-2009.php\">", file=f)
        print("\t<net id=\"net1\" type=\"https://www.pnml.org/version-2009/version-2009.php\">", file=f)
        print("\t\t<page id=\"page1\">", file=f)
        print("\t\t\t<name>", file=f)
        print("\t\t\t\t<text>" + str(petriNet.name) + "</text>", file=f)
        print("\t\t\t</name>", file=f)
        # PLACES
        itemCounter = 1
        PNDict.update({"places": {}})
        print("\t\t\t<!-- Places -->", file=f)
        for place in petriNet.placeList:
            PId = "p" + str(itemCounter)
            itemCounter += 1
            PNDict["places"].update({str(place.name): PId})
            print("\t\t\t<place id=\"" + PId + "\">", file=f)
            # NAME
            print("\t\t\t\t<name>", file=f)
            print("\t\t\t\t\t<text>" + str(place.name) + "</text>", file=f)
            print("\t\t\t\t</name>", file=f)
            # INITIAL MARKING
            # TOKENS
            print("\t\t\t\t<initialMarking>", file=f)
            print("\t\t\t\t\t<text>" + str(place.tokens) + "</text>", file=f)
            print("\t\t\t\t</initialMarking>", file=f)
            # TOTAL TOKENS
            print("\t\t\t\t<initialTotalTokens>", file=f)
            print("\t\t\t\t\t<text>" + str(place.totalTokens) + "</text>", file=f)
            print("\t\t\t\t</initialTotalTokens>", file=f)
            # MAX TOKENS
            print("\t\t\t\t<initialMaxTokens>", file=f)
            print("\t\t\t\t\t<text>" + str(place.maxTokens) + "</text>", file=f)
            print("\t\t\t\t</initialMaxTokens>", file=f)
            print("\t\t\t</place>", file=f)

        # TRANSITIONS
        itemCounter = 1
        PNDict.update({"transitions": {}})
        print("\t\t\t<!-- Transitions -->", file=f)
        # IMMEDIATE TRANSITIONS
        for trans in petriNet.immediateTransList:
            TId = "t" + str(itemCounter)
            itemCounter += 1
            PNDict["transitions"].update({str(trans.name): TId})
            print("\t\t\t<transition id=\"" + TId + "\">", file=f)
            # NAME
            print("\t\t\t\t<name>", file=f)
            print("\t\t\t\t\t<text>" + str(trans.name) + "</text>", file=f)
            print("\t\t\t\t</name>", file=f)
            # TODO: GUARDS
            print("\t\t\t\t<guard>", file=f)
            if (trans.guard is not None):
                guardText = ' '.join(
                    inspect.getsource(trans.guard).split())
            else:
                guardText = "None"
            print("\t\t\t\t\t<text>" + str(guardText) + "</text>", file=f)
            print("\t\t\t\t</guard>", file=f)
            # FIRING PROBABILITY
            print("\t\t\t\t<fireProbability>", file=f)
            print("\t\t\t\t\t<text>" +
                  str(trans.fireProbability) + "</text>", file=f)
            print("\t\t\t\t</fireProbability>", file=f)
            # FIRING COUNT (INITIAL)
            print("\t\t\t\t<fireCount>", file=f)
            print("\t\t\t\t\t<text>" + str(trans.fireCount) + "</text>", file=f)
            print("\t\t\t\t</fireCount>", file=f)
            print("\t\t\t</transition>", file=f)

        # TIMED TRANSITIONS
        for trans in petriNet.timedTransList:
            TId = "t" + str(itemCounter)
            itemCounter += 1
            PNDict["transitions"].update({str(trans.name): TId})
            print("\t\t\t<transition id=\"" + TId + "\">", file=f)
            # NAME
            print("\t\t\t\t<name>", file=f)
            print("\t\t\t\t\t<text>" + str(trans.name) + "</text>", file=f)
            print("\t\t\t\t</name>", file=f)
            # DISTRIBUTION TYPE
            print("\t\t\t\t<distributionType>", file=f)
            print("\t\t\t\t\t<text>" + str(trans.distType) + "</text>", file=f)
            print("\t\t\t\t</distributionType>", file=f)
            # DISTRIBUTION ARGUMENTS
            # A
            print("\t\t\t\t<distributionArg1>", file=f)
            print("\t\t\t\t\t<text>" + str(trans.a) + "</text>", file=f)
            print("\t\t\t\t</distributionArg1>", file=f)
            # B
            print("\t\t\t\t<distributionArg2>", file=f)
            print("\t\t\t\t\t<text>" + str(trans.b) + "</text>", file=f)
            print("\t\t\t\t</distributionArg2>", file=f)
            # C
            print("\t\t\t\t<distributionArg3>", file=f)
            print("\t\t\t\t\t<text>" + str(trans.c) + "</text>", file=f)
            print("\t\t\t\t</distributionArg3>", file=f)
            # D
            print("\t\t\t\t<distributionArg4>", file=f)
            print("\t\t\t\t\t<text>" + str(trans.d) + "</text>", file=f)
            print("\t\t\t\t</distributionArg4>", file=f)
            # TIME UNIT
            print("\t\t\t\t<timeUnit>", file=f)
            print("\t\t\t\t\t<text>" + str(trans.timeUnitType) + "</text>", file=f)
            print("\t\t\t\t</timeUnit>", file=f)
            # AGE POLICY
            print("\t\t\t\t<agePolicy>", file=f)
            print("\t\t\t\t\t<text>" + str(trans.agePolicy) + "</text>", file=f)
            print("\t\t\t\t</agePolicy>", file=f)
            # TODO: GUARD
            print("\t\t\t\t<guard>", file=f)
            if (trans.guard is not None):
                guardText = ' '.join(
                    inspect.getsource(trans.guard).split())
            else:
                guardText = "None"
            print("\t\t\t\t\t<text>" + str(guardText) + "</text>", file=f)
            print("\t\t\t\t</guard>", file=f)
            # FIRING COUNT (INITIAL)
            print("\t\t\t\t<fireCount>", file=f)
            print("\t\t\t\t\t<text>" + str(trans.fireCount) + "</text>", file=f)
            print("\t\t\t\t</fireCount>", file=f)
            print("\t\t\t</transition>", file=f)
        # ARCS
        itemCounter = 1
        PNDict.update({"arcs": {}})
        print("\t\t\t<!-- Arcs -->", file=f)
        # INPUT ARCS
        for input in petriNet.inputArcList:
            AId = "arc" + str(itemCounter)
            itemCounter += 1
            PNDict["arcs"].update({str(input.name): AId})
            sourceId = PNDict['places'][input.fromPlace.name]
            targetId = PNDict['transitions'][input.toTrans.name]
            print("\t\t\t<arc id=\"" + AId + "\" source=\"" +
                  str(sourceId) + "\" target=\"" + str(targetId) + "\">", file=f)
            print("\t\t\t\t<inscription>", file=f)
            print("\t\t\t\t\t<text>" + str(input.multiplicity) + "</text>", file=f)
            print("\t\t\t\t</text>", file=f)
            print("\t\t\t</arc>", file=f)
        # OUTPUT ARCS
        for output in petriNet.outputArcList:
            AId = "arc" + str(itemCounter)
            itemCounter += 1
            PNDict["arcs"].update({str(output.name): AId})
            sourceId = PNDict['transitions'][output.fromTrans.name]
            targetId = PNDict['places'][output.toPlace.name]
            print("\t\t\t<arc id=\"" + AId + "\" source=\"" +
                  str(sourceId) + "\" target=\"" + str(targetId) + "\">", file=f)
            print("\t\t\t\t<inscription>", file=f)
            print("\t\t\t\t\t<text>" + str(output.multiplicity) + "</text>", file=f)
            print("\t\t\t\t</text>", file=f)
            print("\t\t\t</arc>", file=f)
        # INHIBITOR ARCS
        for inhib in petriNet.inhibList:
            AId = "arc" + str(itemCounter)
            itemCounter += 1
            PNDict["arcs"].update({str(inhib.name): AId})
            sourceId = PNDict['places'][inhib.origin.name]
            targetId = PNDict['transitions'][inhib.target.name]
            print("\t\t\t<arc id=\"" + AId + "\" source=\"" +
                  str(sourceId) + "\" target=\"" + str(targetId) + "\">", file=f)
            print("\t\t\t\t<inscription>", file=f)
            print("\t\t\t\t\t<text>" + str(inhib.multiplicity) + "</text>", file=f)
            print("\t\t\t\t</text>", file=f)
            print("\t\t\t</arc>", file=f)
        print("\t\t</page>", file=f)
        print("\t</net>", file=f)
        print("</pnml>", file=f)

        # testing
        print(PNDict, file=f)


def generateLogFile(logText: str, logPath: str, verbose: int, tab: bool = False):

    if (verbose > 0):
        os.makedirs(os.path.dirname(logPath), exist_ok=True)

        with open(logPath, 'a') as f:
            print(logText, file=f)
            if (verbose > 1):
                if (tab):
                    print('\t'.join(logText.splitlines(True)))
                else:
                    print(logText)
