import os
import inspect
import graphviz


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

    # create folder and file for PetriNet (default: root/logs/...)
    os.makedirs(os.path.dirname(fileName), exist_ok=True)
    PNDict = {}

    with open(fileName, 'w') as f:
        print("<?xml version=\"1.0\" encoding=\"UTF-8\"?>", file=f)
        # <pnml>
        print("<pnml xmlns=\"http://www.pnml.org/version-2009/grammar/pnml\">", file=f)
        # <net>
        print("\t<net id=\"net1\" type=\"https://gitlab.sdu.dk/petri-net-python-library/petri-net-python-library\">", file=f)
        # <page>
        print("\t\t<page id=\"page1\">", file=f)
        # <name>
        print("\t\t\t<name>", file=f)
        # <text></text>
        print("\t\t\t\t<text>" + str(petriNet.name) + "</text>", file=f)
        # </name>
        print("\t\t\t</name>", file=f)
        # <toolspecific>
        print("\t\t\t<toolspecific tool=\"https://gitlab.sdu.dk/petri-net-python-library/petri-net-python-library\" version=\"1.0\" />", file=f)

        # PLACES
        itemCounter = 1
        PNDict.update({"places": {}})
        print("\t\t\t<!-- Places -->", file=f)
        for place in petriNet.placeList:
            PId = "p" + str(itemCounter)
            itemCounter += 1
            PNDict["places"].update({str(place.name): PId})
            # <place>
            print("\t\t\t<place id=\"" + PId + "\">", file=f)
            # <name>
            print("\t\t\t\t<name>", file=f)
            # <text></text>
            print("\t\t\t\t\t<text>" + str(place.name) + "</text>", file=f)
            # </name>
            print("\t\t\t\t</name>", file=f)

            # INITIAL MARKING
            # <initialMarking> (tokens)
            print("\t\t\t\t<initialMarking>", file=f)
            # <text></text>
            print("\t\t\t\t\t<text>" + str(place.tokens) + "</text>", file=f)
            # </initialMarking> (tokens)
            print("\t\t\t\t</initialMarking>", file=f)

            # <initialTotalTokens> (totalTokens)
            print("\t\t\t\t<initialTotalTokens>", file=f)
            # <text></text>
            print("\t\t\t\t\t<text>" + str(place.totalTokens) + "</text>", file=f)
            # </initialTotalTokens> (totalTokens)
            print("\t\t\t\t</initialTotalTokens>", file=f)

            # <initialMaxTokens> (maxTokens)
            print("\t\t\t\t<initialMaxTokens>", file=f)
            # <text></text>
            print("\t\t\t\t\t<text>" + str(place.maxTokens) + "</text>", file=f)
            # </nitialMaxTokens> (maxTokens)
            print("\t\t\t\t</initialMaxTokens>", file=f)
            # </place>
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
            # <transition>
            print("\t\t\t<transition id=\"" + TId +
                  "\" type=\"immediate\">", file=f)

            # <name>
            print("\t\t\t\t<name>", file=f)
            # <text></text>
            print("\t\t\t\t\t<text>" + str(trans.name) + "</text>", file=f)
            # </name>
            print("\t\t\t\t</name>", file=f)

            # <guard> TODO:
            print("\t\t\t\t<guard>", file=f)
            if (trans.guard is not None):

                # <name>
                print("\t\t\t\t\t<name>", file=f)
                # <text></text>
                print("\t\t\t\t\t\t<text>" +
                      str(trans.guard.__name__) + "</text>", file=f)
                # </name>
                print("\t\t\t\t\t</name>", file=f)

                # <code>
                print("\t\t\t\t\t<code>", file=f)
                # <text></text>
                print("\t\t\t\t\t\t<text>" +
                      str(' '.join(inspect.getsource(trans.guard).split())) + "</text>", file=f)
                # </code>
                print("\t\t\t\t\t</code>", file=f)

            else:
                # <text></text>
                print("\t\t\t\t\t<text>" + str(None) + "</text>", file=f)

            # </guard>
            print("\t\t\t\t</guard>", file=f)

            # <fireProbability>
            print("\t\t\t\t<fireProbability>", file=f)
            # <text></text>
            print("\t\t\t\t\t<text>" +
                  str(trans.fireProbability) + "</text>", file=f)
            # </fireProbability>
            print("\t\t\t\t</fireProbability>", file=f)

            # <fireCount> (initialFireCount)
            print("\t\t\t\t<fireCount>", file=f)
            # <text></text>
            print("\t\t\t\t\t<text>" + str(trans.fireCount) + "</text>", file=f)
            # </fireCount> (initialFireCount)
            print("\t\t\t\t</fireCount>", file=f)
            # </transition>
            print("\t\t\t</transition>", file=f)

        # TIMED TRANSITIONS
        for trans in petriNet.timedTransList:
            TId = "t" + str(itemCounter)
            itemCounter += 1
            PNDict["transitions"].update({str(trans.name): TId})
            # <transition>
            print("\t\t\t<transition id=\"" + TId +
                  "\" type=\"timed\">", file=f)
            # <name>
            print("\t\t\t\t<name>", file=f)
            # <text></text>
            print("\t\t\t\t\t<text>" + str(trans.name) + "</text>", file=f)
            # </name>
            print("\t\t\t\t</name>", file=f)

            # <distributionType>
            print("\t\t\t\t<distributionType>", file=f)
            # <text></text>
            print("\t\t\t\t\t<text>" + str(trans.distType) + "</text>", file=f)
            # </distributionType>
            print("\t\t\t\t</distributionType>", file=f)

            # DISTRIBUTION ARGUMENTS
            # <distributionArg1> (distArgA)
            print("\t\t\t\t<distributionArg1>", file=f)
            # <text></text>
            print("\t\t\t\t\t<text>" + str(trans.a) + "</text>", file=f)
            # </distributionArg1> (distArgA)
            print("\t\t\t\t</distributionArg1>", file=f)

            # <distributionArg2> (distArgB)
            print("\t\t\t\t<distributionArg2>", file=f)
            # <text></text>
            print("\t\t\t\t\t<text>" + str(trans.b) + "</text>", file=f)
            # <distributionArg2> (distArgB)
            print("\t\t\t\t</distributionArg2>", file=f)

            # <distributionArg3> (distArgC)
            print("\t\t\t\t<distributionArg3>", file=f)
            # <text></text>
            print("\t\t\t\t\t<text>" + str(trans.c) + "</text>", file=f)
            # <distributionArg3> (distArgC)
            print("\t\t\t\t</distributionArg3>", file=f)

            # <distributionArg4> (distArgD)
            print("\t\t\t\t<distributionArg4>", file=f)
            # <text></text>
            print("\t\t\t\t\t<text>" + str(trans.d) + "</text>", file=f)
            # <distributionArg4> (distArgD)
            print("\t\t\t\t</distributionArg4>", file=f)

            # <timeUnit>
            print("\t\t\t\t<timeUnit>", file=f)
            # <text></text>
            print("\t\t\t\t\t<text>" + str(trans.timeUnitType) + "</text>", file=f)
            # </timeUnit>
            print("\t\t\t\t</timeUnit>", file=f)

            # <agePolicy>
            print("\t\t\t\t<agePolicy>", file=f)
            # <text></text>
            print("\t\t\t\t\t<text>" + str(trans.agePolicy) + "</text>", file=f)
            # </agePolicy>
            print("\t\t\t\t</agePolicy>", file=f)

            # <guard> TODO:
            print("\t\t\t\t<guard>", file=f)
            if (trans.guard is not None):

                # <name>
                print("\t\t\t\t\t<name>", file=f)
                # <text></text>
                print("\t\t\t\t\t\t<text>" +
                      str(trans.guard.__name__) + "</text>", file=f)
                # </name>
                print("\t\t\t\t\t</name>", file=f)

                # <code>
                print("\t\t\t\t\t<code>", file=f)
                # <text></text>
                print("\t\t\t\t\t\t<text>" +
                      str(' '.join(inspect.getsource(trans.guard).split())) + "</text>", file=f)
                # </code>
                print("\t\t\t\t\t</code>", file=f)

            else:
                # <text></text>
                print("\t\t\t\t\t<text>" + str(None) + "</text>", file=f)

            # </guard>
            print("\t\t\t\t</guard>", file=f)

            # <fireCount> (initialFireCount)
            print("\t\t\t\t<fireCount>", file=f)
            # <text></text>
            print("\t\t\t\t\t<text>" + str(trans.fireCount) + "</text>", file=f)
            # </fireCount> (initialFireCount)
            print("\t\t\t\t</fireCount>", file=f)
            # </transition>
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
            # <arc>
            print("\t\t\t<arc id=\"" + AId + "\" source=\"" +
                  str(sourceId) + "\" target=\"" + str(targetId) + "\" type=\"input\">", file=f)
            # <name>
            print("\t\t\t\t<name>", file=f)
            # <text></text>
            print("\t\t\t\t\t<text>" + str(input.name) + "</text>", file=f)
            # </name>
            print("\t\t\t\t</name>", file=f)
            # <inscription>
            print("\t\t\t\t<inscription>", file=f)
            if (input.multiplicity.__class__.__name__ == 'int'):
                # <text></text>
                print("\t\t\t\t\t<text>" +
                      str(input.multiplicity) + "</text>", file=f)
            elif (input.multiplicity.__class__.__name__ == 'function'):
                # <text></text>
                print("\t\t\t\t\t<text>" + str(' '.join(inspect.getsource(
                    input.multiplicity).split())) + "</text>", file=f)
            # </inscription>
            print("\t\t\t\t</inscription>", file=f)
            # </arc>
            print("\t\t\t</arc>", file=f)

        # OUTPUT ARCS
        for output in petriNet.outputArcList:
            AId = "arc" + str(itemCounter)
            itemCounter += 1
            PNDict["arcs"].update({str(output.name): AId})
            sourceId = PNDict['transitions'][output.fromTrans.name]
            targetId = PNDict['places'][output.toPlace.name]
            # <arc>
            print("\t\t\t<arc id=\"" + AId + "\" source=\"" +
                  str(sourceId) + "\" target=\"" + str(targetId) + "\" type=\"output\">", file=f)
            # <name>
            print("\t\t\t\t<name>", file=f)
            # <text></text>
            print("\t\t\t\t\t<text>" + str(output.name) + "</text>", file=f)
            # </name>
            print("\t\t\t\t</name>", file=f)
            # <inscription>
            print("\t\t\t\t<inscription>", file=f)
            if (output.multiplicity.__class__.__name__ == 'int'):
                # <text></text>
                print("\t\t\t\t\t<text>" +
                      str(output.multiplicity) + "</text>", file=f)
            elif (output.multiplicity.__class__.__name__ == 'function'):
                # <text></text>
                print("\t\t\t\t\t<text>" + str(' '.join(inspect.getsource(
                    output.multiplicity).split())) + "</text>", file=f)
            # </inscription>
            print("\t\t\t\t</inscription>", file=f)
            # </arc>
            print("\t\t\t</arc>", file=f)

        # INHIBITOR ARCS
        for inhib in petriNet.inhibList:
            AId = "arc" + str(itemCounter)
            itemCounter += 1
            PNDict["arcs"].update({str(inhib.name): AId})
            sourceId = PNDict['places'][inhib.origin.name]
            targetId = PNDict['transitions'][inhib.target.name]
            # <arc>
            print("\t\t\t<arc id=\"" + AId + "\" source=\"" +
                  str(sourceId) + "\" target=\"" + str(targetId) + "\" type=\"inhibitor\">", file=f)
            # <name>
            print("\t\t\t\t<name>", file=f)
            # <text></text>
            print("\t\t\t\t\t<text>" + str(inhib.name) + "</text>", file=f)
            # </name>
            print("\t\t\t\t</name>", file=f)
            # <inscription>
            print("\t\t\t\t<inscription>", file=f)
            if (inhib.multiplicity.__class__.__name__ == 'int'):
                # <text></text>
                print("\t\t\t\t\t<text>" +
                      str(inhib.multiplicity) + "</text>", file=f)
            elif (inhib.multiplicity.__class__.__name__ == 'function'):
                # <text></text>
                print("\t\t\t\t\t<text>" + str(' '.join(inspect.getsource(
                    inhib.multiplicity).split())) + "</text>", file=f)
            # </inscription>
            print("\t\t\t\t</inscription>", file=f)
            # </arc>
            print("\t\t\t</arc>", file=f)

        # </page>
        print("\t\t</page>", file=f)
        # </net>
        print("\t</net>", file=f)
        # </pnml>
        print("</pnml>", file=f)


def generatePNGraph(petriNet, fileName: str):

    graph = graphviz.Digraph(
        format='png', comment=petriNet.name + " Petri Net")
    graph.attr(rankdir='LR')

    for place in petriNet.placeList:
        graph.node(place.name, label=place.name, shape='circle',
                   fontname='times bold')

    for trans in petriNet.timedTransList:
        graph.node(trans.name, label=trans.name,
                   fillcolor='white', fontcolor='black', fontname='times bold', shape='rectangle', style='filled')

    for trans in petriNet.immediateTransList:
        graph.node(trans.name, label=trans.name,
                   fillcolor='black', fontcolor='white', fontname='times bold', shape='rectangle', style='filled')

    for input in petriNet.inputArcList:
        graph.edge(input.fromPlace.name,
                   input.toTrans.name, arrowhead='normal')
    for output in petriNet.outputArcList:
        graph.edge(output.fromTrans.name,
                   output.toPlace.name, arrowhead='normal')
    for inhib in petriNet.inhibList:
        graph.edge(inhib.origin.name, inhib.target.name,
                   arrowhead='odot')

    graph.render(fileName + 'graphviz_output/' + petriNet.name +
                 '.gv', view=True).replace('\\', '/')


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
