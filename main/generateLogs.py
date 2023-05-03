import os


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
    pass


def generateLogFile(logText: str, logPath: str, verbose: int, tab: bool = False):

    os.makedirs(os.path.dirname(logPath), exist_ok=True)

    with open(logPath, 'a') as f:
        print(logText, file=f)
        if(verbose > 0):
            if(tab):
                print('\t'.join(logText.splitlines(True)))
            else:
                print(logText)
