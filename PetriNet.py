from components.immediateTransition import ImmediateTransition
from components.timedTransition import TimedTransition
from components.place import Place
from components.inputArc import InputArc
from components.outputArc import OutputArc
from components.inhibArc import InhibArc

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
        self.getPlaces()
        print("Timed Transitions:\n")
        self.getTimedTransitions()
        print("Immediate Transitions:\n")
        self.getImmediateTransitions()
        print("Input Arcs:\n")
        self.getInputArcs()
        print("Output Arcs:\n")
        self.getOutputArcs()
        print("Inhibitor Arcs:\n")
        self.getInhibArcs()

    def getPlaces(self):
        for place in self.placeList:
            print(place)

    def getTimedTransitions(self):
        for timedTrans in self.timedTransList:
            print(timedTrans)

    def getImmediateTransitions(self):
        for immediateTrans in self.immediateTransList:
            print(immediateTrans)

    def getInputArcs(self):
        for inputArc in self.inputArcList:
            print(inputArc)

    def getOutputArcs(self):
        for outputArc in self.outputArcList:
            print(outputArc)

    def getInhibArcs(self):
        for inhibArc in self.inhibList:
            print(inhibArc)
