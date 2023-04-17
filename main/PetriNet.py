from components.immediateTransition import ImmediateTransition
from components.timedTransition import TimedTransition
from components.place import Place
from components.inputArc import InputArc
from components.outputArc import OutputArc
from components.inhibArc import InhibArc
from .simulation import simulation

petriNetList = []


class PetriNet:
    def __init__(self, name: str):

        self.name = str(name)

        self.placeList = []
        self.timedTransList = []
        self.immediateTransList = []
        self.inputArcList = []
        self.outputArcList = []
        self.inhibList = []

        petriNetList.append(self)

    def describe(self):
        '''
        Describes the current state of the Petri Net instance.
        '''
        print("Places:\n")
        print('\t'.join(self.getPlaces().splitlines(True)))
        print("Timed Transitions:\n")
        print('\t'.join(self.getTimedTransitions().splitlines(True)))
        print("Immediate Transitions:\n")
        print('\t'.join(self.getImmediateTransitions().splitlines(True)))
        print("Input Arcs:\n")
        print('\t'.join(self.getInputArcs().splitlines(True)))
        print("Output Arcs:\n")
        print('\t'.join(self.getOutputArcs().splitlines(True)))
        print("Inhibitor Arcs:\n")
        print('\t'.join(self.getInhibArcs().splitlines(True)))

    def getPlaces(self):
        returnString = ''
        for place in self.placeList:
            returnString += '\t' + str(place) + '\n'
        return returnString

    def getTimedTransitions(self):
        returnString = ''
        for timedTrans in self.timedTransList:
            returnString += '\t' + str(timedTrans) + '\n'
        return returnString

    def getImmediateTransitions(self):
        returnString = ''
        for immediateTrans in self.immediateTransList:
            returnString += '\t' + str(immediateTrans) + '\n'
        return returnString

    def getInputArcs(self):
        returnString = ''
        for inputArc in self.inputArcList:
            returnString += '\t' + str(inputArc) + '\n'
        return returnString

    def getOutputArcs(self):
        returnString = ''
        for outputArc in self.outputArcList:
            returnString += '\t' + str(outputArc) + '\n'
        return returnString

    def getInhibArcs(self):
        returnString = ''
        for inhibArc in self.inhibList:
            returnString += '\t' + str(inhibArc) + '\n'
        return returnString

    def runSimulation(self, simLength: int, randomSeed: int = 1337, verbose: int = 1,  defTimeUnit: str = 'sec', logPath: str = './logs'):

        simulation(self, simLength, randomSeed, verbose, defTimeUnit, logPath)
