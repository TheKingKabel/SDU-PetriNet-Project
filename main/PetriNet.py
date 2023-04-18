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
        print("Places:")
        print('\t'.join(self.getPlaces().splitlines(True)))
        print("Timed Transitions:")
        print('\t'.join(self.getTimedTransitions().splitlines(True)))
        print("Immediate Transitions:")
        print('\t'.join(self.getImmediateTransitions().splitlines(True)))
        print("Input Arcs:")
        print('\t'.join(self.getInputArcs().splitlines(True)))
        print("Output Arcs:")
        print('\t'.join(self.getOutputArcs().splitlines(True)))
        print("Inhibitor Arcs:")
        print('\t'.join(self.getInhibArcs().splitlines(True)))

    def getPlaces(self):
        returnString = ''
        if(len(self.placeList) == 0):
            return '\tNone\n'
        for place in self.placeList:
            returnString += '\n' + str(place)
        return returnString

    def getTimedTransitions(self):
        returnString = ''
        if(len(self.timedTransList) == 0):
            return '\tNone\n'
        for timedTrans in self.timedTransList:
            returnString += '\n' + str(timedTrans)
        return returnString

    def getImmediateTransitions(self):
        returnString = ''
        if(len(self.immediateTransList) == 0):
            return '\tNone\n'
        for immediateTrans in self.immediateTransList:
            returnString += '\n' + str(immediateTrans)
        return returnString

    def getInputArcs(self):
        returnString = ''
        if(len(self.inputArcList) == 0):
            return '\tNone\n'
        for inputArc in self.inputArcList:
            returnString += '\n' + str(inputArc)
        return returnString

    def getOutputArcs(self):
        returnString = ''
        if(len(self.outputArcList) == 0):
            return '\tNone\n'
        for outputArc in self.outputArcList:
            returnString += '\n' + str(outputArc)
        return returnString

    def getInhibArcs(self):
        returnString = ''
        if(len(self.inhibList) == 0):
            return '\tNone\n'
        for inhibArc in self.inhibList:
            returnString += '\n' + str(inhibArc)
        return returnString

    def runSimulation(self, simLength: int, randomSeed: int = 1337, verbose: int = 1,  defTimeUnit: str = 'sec', logPath: str = './logs'):

        simulation(self, simLength, randomSeed, verbose, defTimeUnit, logPath)
