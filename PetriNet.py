petriNetList = []


class PetriNet:
    def __init__(self, name: str):

        self.name = name

        self.placeList = []
        self.timedTransList = []
        self.immediateTransList = []
        self.inputEdgeList = []
        self.outputEdgeList = []
        self.inhibList = []

        petriNetList.append(self)

    def getPlaces(self):
        for place in self.placeList:
            print(place)

    def getTimedTransitions(self):
        for timedTrans in self.timedTransList:
            print(timedTrans)

    def getInstantTransitions(self):
        for instantTrans in self.immediateTransList:
            print(instantTrans)

    def getInputEdges(self):
        for inputEdge in self.inputEdgeList:
            print(inputEdge)

    def getOutputEdges(self):
        for outputEdge in self.outputEdgeList:
            print(outputEdge)

    def getInhibEdges(self):
        for inhibEdge in self.inhibList:
            print(inhibEdge)
