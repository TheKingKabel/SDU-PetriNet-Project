from main import placeList

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
            self.inBoundOutputArcs = []         # list of inbound output arcs targeting the current place
            self.outBoundInhibArcs = []         # list of outbound inhibitor arcs originating from current place
            self.inBoundInhibArcs = []          # list of inbound inhibitor arcs taregting the current place
            placeList.append(self)

        else:
            del self
            raise Exception("A Place already exists named: " + name) # places must have a uniqe name to differentiate

    def __str__(self):
        returnString = (
            f"Place (name={self.name}, "
            f"start place={self.start}, "
            f"current nbr of tokens={self.tokens}, "
            f"total tokens held={self.totalTokens}, "
            f"max tokens held={self.maxTokens}, "
            f"list of outbound input arcs={str(self.outBoundInputArcs)}, "
            f"list of inbound output arcs={str(self.inBoundOutputArcs)}, "
            f"list of outbound inhibitor arcs={str(self.outBoundInhibArcs)}, "
            f"list of inbound inhibitor arcs={str(self.inBoundInhibArcs)}"
        )
        return returnString
    # NAME
    def setName(self, newName: str):
        if (checkName(newName)):
            self.name = newName
        else:
            raise Exception("A Place already exists named: " + newName)

    def getName(self):
        return self.name
    
    # STRART
    def setStart(self, start: bool):
        self.start = start

    def getStart(self):
        return self.start

    # TOKENS
    def setTokens(self, tokens: int):
        self.tokens = tokens

    def getTokens(self):
        return self.tokens
    
    # TOTAL TOKENS
    def setTotalTokens(self, totalTokens: int):
        self.totalTokens = totalTokens

    def getTotalTokens(self):
        return self.totalTokens

    # MAX TOKENS
    def setMaxTokens(self, maxTokens: int):
        self.maxTokens = maxTokens

    def getMaxTokens(self):
        return self.maxTokens

    # OUTBOUND INPUT ARCS
    def setOutBoundInputArcs(self, *outBoundInputArcList):
        self.outBoundInputArcs.clear
        for arc in outBoundInputArcList:
            self.outBoundInputArcs.append(arc)
    
    def getOutBoundInputArcs(self):
        return self.outBoundInputArcs

    def addOutBoundInputArcs(self, newOutBoundInputArc):
        self.outBoundInputArcs.append(newOutBoundInputArc)
    
    # INBOUND OUTPUT ARCS
    def setInBoundOutputArcs(self, *inBoundOutputArcList):
        self.inBoundOutputArcs.clear
        for arc in inBoundOutputArcList:
            self.inBoundOutputArcs.append(arc)
    
    def setInBoundOutputArcs(self):
        return self.inBoundOutputArcs

    def addInBoundOutputArcs(self, newInBoundOutputArc):
        self.inBoundOutputArcs.append(newInBoundOutputArc)

    # OUTBOUND INHIB ARCS
    def setOutBoundInhibArcs(self, *outBoundInhibArcList):
        self.outBoundInhibArcs.clear
        for arc in outBoundInhibArcList:
            self.outBoundInhibArcs.append(arc)
    
    def getOutBoundInhibArcs(self):
        return self.outBoundInhibArcs

    def addOutBoundInhibArcs(self, newOutBoundInhibArc):
        self.outBoundInhibArcs.append(newOutBoundInhibArc)

    # INBOUND INHIB ARCS
    def setInBoundInhibArcs(self, *inBoundInhibArcList):
        self.inBoundInhibArcs.clear
        for arc in inBoundInhibArcList:
            self.inBoundInhibArcs.append(arc)
    
    def getInBoundInhibArcs(self):
        return self.inBoundInhibArcs

    def addInBoundInhibArcs(self, newInBoundInhibArc):
        self.inBoundInhibArcs.append(newInBoundInhibArc)

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

# NAME
def setName(placeName: str, newName: str):
    place = findPlaceByName(placeName)
    if (checkName(newName)):
        place.name = newName
    else:
        raise Exception("A Place already exists named: " + newName)

def getName(placeName: str):
    place = findPlaceByName(placeName)
    return place.name
    
# START
def setStart(placeName: str, start: bool):
    place = findPlaceByName(placeName)
    place.start = start

def getStart(placeName: str):
    place = findPlaceByName(placeName)
    return place.start

# TOKENS
def setTokens(placeName: str, tokens: int):
    place = findPlaceByName(placeName)
    place.tokens = tokens

def getTokens(placeName: str):
    place = findPlaceByName(placeName)
    return place.tokens
    
# TOTAL TOKENS
def setTotalTokens(placeName: str, totalTokens: int):
    place = findPlaceByName(placeName)
    place.totalTokens = totalTokens

def getTotalTokens(placeName: str):
    place = findPlaceByName(placeName)
    return place.totalTokens

# MAX TOKENS
def setMaxTokens(placeName: str, maxTokens: int):
    place = findPlaceByName(placeName)
    place.maxTokens = maxTokens

def getMaxTokens(placeName: str):
    place = findPlaceByName(placeName)
    return place.maxTokens

# OUTBOUND INPUT ARCS
def setOutBoundInputArcs(placeName: str, *outBoundInputArcList):
    place = findPlaceByName(placeName)
    place.outBoundInputArcs.clear
    for arc in outBoundInputArcList:
        place.outBoundInputArcs.append(arc)
    
def getOutBoundInputArcs(placeName: str):
    place = findPlaceByName(placeName)
    return place.outBoundInputArcs

def addOutBoundInputArcs(placeName: str, newOutBoundInputArc):
    place = findPlaceByName(placeName)
    place.outBoundInputArcs.append(newOutBoundInputArc)

# INBOUND OUTPUT ARCS
def setInBoundOutputArcs(placeName: str, *inBoundOutputArcList):
    place = findPlaceByName(placeName)
    place.inBoundOutputArcs.clear
    for arc in inBoundOutputArcList:
        place.inBoundOutputArcs.append(arc)
    
def getInBoundOutputArcs(placeName: str):
    place = findPlaceByName(placeName)
    return place.inBoundOutputArcs

def addInBoundOutputArcs(placeName: str, newInBoundOutputArc):
    place = findPlaceByName(placeName)
    place.inBoundOutputArcs.append(newInBoundOutputArc)

# OUTBOUND INHIB ARCS
def setOutBoundInhibArcs(placeName: str, *outBoundInhibArcList):
    place = findPlaceByName(placeName)
    place.outBoundInhibArcs.clear
    for arc in outBoundInhibArcList:
        place.outBoundInhibArcs.append(arc)
    
def getOutBoundInhibArcs(placeName: str):
    place = findPlaceByName(placeName)
    return place.outBoundInhibArcs

def addOutBoundInhibArcs(placeName: str, newOutBoundInhibArc):
    place = findPlaceByName(placeName)
    place.outBoundInhibArcs.append(newOutBoundInhibArc)

# INBOUND INHIB ARCS
def setInBoundInhibArcs(placeName: str, *inBoundInhibArcList):
    place = findPlaceByName(placeName)
    place.inBoundInhibArcs.clear
    for arc in inBoundInhibArcList:
        place.inBoundInhibArcs.append(arc)
    
def getInBoundInhibArcs(placeName: str):
    place = findPlaceByName(placeName)
    return place.inBoundInhibArcs

def addInBoundInhibArcs(placeName: str, newInBoundInhibArc):
    place = findPlaceByName(placeName)
    place.inBoundInhibArcs.append(newInBoundInhibArc)
