from main import placeList
import inputArc
import inhibArc
import outputArc

class Place:

    def __init__(self, name: str, start: bool=False, tokens: int=0, totalTokens: int=0, maxTokens: int=0):
        if (checkName(name)):
            self.name = name                    # name of the place, must be unique
            self.start = start                  # start place, default false, used to determine start of simulation
            self.tokens = tokens                # nbr of initial tokens, default 0, if set, totalTokens and maxTokens get the same value
            if (tokens == 0):
                self.totalTokens = totalTokens  # var used to count the total number of tokens in place for statistics, default 0
            else:
                self.totalTokens = tokens
            if (tokens == 0):
                self.maxTokens = maxTokens      # var used to count the maximum tokens in place for statistics, default 0
            else:
                self.maxTokens = tokens
            self.outBoundInputArcs = []         # list of outbound input arcs originating from current place
            self.inBoundOutPutArcs = []         # list of inbound output arcs targeting the current place
            self.outBoundInhibArcs = []         # list of outbound inhibitor arcs originating from current place
            self.inBoundInhibArcs = []          # list of inbound inhibitor arcs taregting the current place
            placeList.append(self)

        else:
            del self
            raise Exception("A Place already exists named: " + name) # places must have a uniqe name to differentiate

    def __str__(self):
        return (
            f'Place (name={self.name}, \
            start place={self.start}, \
            current nbr of tokens={self.tokens}, \
            total tokens held={self.totalTokens}, \
            max tokens held={self.maxTokens}, \
            list of outbound input arcs={str(self.outBoundInputArcs)}, \
            list of inbound output arcs={str(self.inBoundOutPutArcs)}, \
            list of outbound inhibitor arcs={str(self.outBoundInhibArcs)}, \
            list of inbound inhibitor arcs={str(self.outBoundInhibArcs)}'
            )

    def setName(self, newName: str):
        if (checkName(newName)):
            self.name = newName
        else:
            raise Exception("A Place already exists named: " + newName)
    
    def getName(self):
        return self.name
    
    def setStart(self, start: bool):
        self.start = start

    def getStart(self):
        return self.start

    def setTokens(self, tokens: int):
        self.tokens = tokens

    def getTokens(self):
        return self.tokens
    
    def setTotalTokens(self, totalTokens: int):
        self.totalTokens = totalTokens

    def getTotalTokens(self):
        return self.totalTokens

    def setMaxTokens(self, maxTokens: int):
        self.maxTokens = maxTokens

    def getMaxTokens(self):
        return self.maxTokens

    def setOutBoundInputArcs(self, *outBoundInputArcList: inputArc.InputArc):
        self.outBoundInputArcs.clear
        for arc in outBoundInputArcList:
            self.outBoundInputArcs.append(arc)
    
    def getOutBoundInputArcs(self):
        return self.outBoundInputArcs

    def addOutBoundInputArcs(self, arc: inputArc.InputArc):
        self.outBoundInputArcs.append(arc)
    
    
    def setInBoundOutPutArcs(self, *inBoundOutPutArcList: outputArc.OutputArc):
        self.inBoundOutPutArcs.clear
        for arc in inBoundOutPutArcList:
            self.inBoundOutPutArcs.append(arc)
    
    def setInBoundOutPutArcs(self):
        return self.inBoundOutPutArcs

    def addInBoundOutPutArcs(self, arc: outputArc.OutputArc):
        self.inBoundOutPutArcs.append(arc)

    
    def setOutBoundInhibArcs(self, *outBoundInhibArcList: inhibArc.InhibArc):
        self.outBoundInhibArcs.clear
        for arc in outBoundInhibArcList:
            self.outBoundInhibArcs.append(arc)
    
    def getOutBoundInhibArcs(self):
        return self.outBoundInhibArcs

    def addOutBoundInhibArcs(self, arc: inhibArc.InhibArc):
        self.outBoundInhibArcs.append(arc)


    def setInBoundInhibArcs(self, *inBoundInhibArcList: inhibArc.InhibArc):
        self.inBoundInhibArcs.clear
        for arc in inBoundInhibArcList:
            self.inBoundInhibArcs.append(arc)
    
    def getInBoundInhibArcs(self):
        return self.inBoundInhibArcs

    def addInBoundInhibArcs(self, arc: inhibArc.InhibArc):
        self.inBoundInhibArcs.append(arc)

def checkName(name):
    for place in placeList:
        if (place.name == name):
            return False
    return True

def findPlaceByName(name):
    for place in placeList:
        if (place.name == name):
            return place
    raise Exception('Place does not exists with name: ' + name)


def setName(placeName: str, newName: str):
    place = findPlaceByName(placeName)
    if (checkName(newName)):
        place.name = newName
    else:
        raise Exception("A Place already exists named: " + newName)

def getName(placeName: str):
    place = findPlaceByName(placeName)
    return place.name
    
def setStart(placeName: str, start: bool):
    place = findPlaceByName(placeName)
    place.start = start

def getStart(placeName: str):
    place = findPlaceByName(placeName)
    return place.start

def setTokens(placeName: str, tokens: int):
    place = findPlaceByName(placeName)
    place.tokens = tokens

def getTokens(placeName: str):
    place = findPlaceByName(placeName)
    return place.tokens
    
def setTotalTokens(placeName: str, totalTokens: int):
    place = findPlaceByName(placeName)
    place.totalTokens = totalTokens

def getTotalTokens(placeName: str):
    place = findPlaceByName(placeName)
    return place.totalTokens

def setMaxTokens(placeName: str, maxTokens: int):
    place = findPlaceByName(placeName)
    place.maxTokens = maxTokens

def getMaxTokens(placeName: str):
    place = findPlaceByName(placeName)
    return place.maxTokens

def setOutBoundInputArcs(placeName: str, *outBoundInputArcList: inputArc.InputArc):
    place = findPlaceByName(placeName)
    place.outBoundInputArcs.clear
    for arc in outBoundInputArcList:
        place.outBoundInputArcs.append(arc)
    
def getOutBoundInputArcs(placeName: str):
    place = findPlaceByName(placeName)
    return place.outBoundInputArcs

def addOutBoundInputArcs(placeName: str, arc: inputArc.InputArc):
    place = findPlaceByName(placeName)
    place.outBoundInputArcs.append(arc)