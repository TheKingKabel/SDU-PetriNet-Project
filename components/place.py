from main import placeList

class Place:

    def __init__(self, name: str, start: bool=False, tokens: int=0, totalTokens: int=0, maxTokens: int=0):
        '''
        Create an instance of the Place class.
        @param name: Unique name of the Place, must be string
        @param start: Variable used to mark starting point of Petri Net, must be boolean                TODO: implement PN net / chain depth detection?
        @param tokens: Current number of tokens held by Place, must be integer
        @param totalTokens: Total number of tokens held by Place for statistics, must be integer        TODO: remove from constructor, it's updated automatically
        @param maxTokens: Maximum number of tokens held by Place for statistics, must be integer        TODO: remove from constructor, it's updated automatically
        '''
        if (checkName(name)):
            self.name = name                                                                            # name of the place, must be unique
            self.start = start                                                                          # start place, default false, used to determine start of simulation
            self.tokens = tokens                                                                        # nbr of initial tokens, default 0, if set, totalTokens and maxTokens get the same value
            if (tokens == 0):
                self.totalTokens = totalTokens                                                          # var used to count the total number of tokens in place for statistics, default 0
            else:
                self.totalTokens = tokens
            if (tokens == 0):
                self.maxTokens = maxTokens                                                              # var used to count the maximum tokens in place for statistics, default 0
            else:
                self.maxTokens = tokens
            
            self.outBoundInputArcs = []                                                                 # list of outbound input arcs originating from current place
            self.inBoundOutputArcs = []                                                                 # list of inbound output arcs targeting the current place
            self.outBoundInhibArcs = []                                                                 # list of outbound inhibitor arcs originating from current place
            self.inBoundInhibArcs = []                                                                  # list of inbound inhibitor arcs taregting the current place
            
            placeList.append(self)

        else:
            del self
            raise Exception("A Place already exists named: " + name)                                    # places must have a uniqe name to differentiate

    def __str__(self):
        '''
        Default return value of class, gives description of current state of Place.
        '''
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
        '''
        Setter function for name of Place.
        @param newName: Unique new name for Place, must be string
        '''
        if (checkName(newName)):
            self.name = newName
        else:
            raise Exception("A Place already exists named: " + newName)

    def getName(self):
        '''
        Getter function for name of Place.
        Returns current name of Place.
        '''
        return self.name
    
    # START
    def setStart(self, start: bool):
        '''
        Setter function for start variable of Place.
        @param start: New value for start variable of Place, must be boolean
        '''
        self.start = start

    def getStart(self):
        '''
        Getter function for start variable of Place.
        Returns current start variable of Place.
        '''
        return self.start

    # TOKENS
    def setTokens(self, tokens: int):
        '''
        Setter function for number of tokens held of Place.
        @param tokens: New value for number of tokens held of Place, must be integer
        '''
        self.tokens = tokens

    def getTokens(self):
        '''
        Getter function for number of tokens held of Place.
        Returns current number of tokens held of Place.
        '''
        return self.tokens
    
    # TOTAL TOKENS
    def setTotalTokens(self, totalTokens: int):
        '''
        Setter function for total number of tokens held of Place, for statistics.
        @param totalTokens: New value for total number of tokens held of Place, must be integer
        '''
        self.totalTokens = totalTokens

    def getTotalTokens(self):
        '''
        Getter function for total number of tokens held of Place, for statistics.
        Returns current total number of tokens held of Place.
        '''
        return self.totalTokens

    # MAX TOKENS
    def setMaxTokens(self, maxTokens: int):
        '''
        Setter function for maximum number of tokens held of Place, for statistics.
        @param maxTokens: New value for maximum number of tokens held of Place, must be integer
        '''
        self.maxTokens = maxTokens

    def getMaxTokens(self):
        '''
        Getter function for maximum number of tokens held of Place, for statistics.
        Returns current maximum number of tokens held of Place.
        '''
        return self.maxTokens

    # OUTBOUND INPUT ARCS
    def setOutBoundInputArcs(self, *outBoundInputArcList):
        '''
        Setter function to overwrite outbound input arcs originating from current Place.
        Note: this function deletes existing list of outbound input arcs, and creates new list with the given parameters. To add single new Input Arc to Place's outbound Input Arc list, use addOutBoundInputArcs.
        @param *outBoundInputArcList: New tuple of Input Arcs to be added to Place's outbound Input Arc list, must be a tuple of instances of class Input Arc
        '''
        for arc in outBoundInputArcList:
            if(checkType(arc) != "InputArc"):
                raise Exception("Place's new outbound Input Arc list's elements must be instances of class Input Arc")
        self.outBoundInputArcs.clear
        for arc in outBoundInputArcList:
            arc.setFromPlace(self)
            self.outBoundInputArcs.append(arc)
    
    def getOutBoundInputArcs(self):
        '''
        Getter function for list of outbound input arcs originating from current Place.
        Returns current list of outbound input arcs originating from current Place.
        '''
        return self.outBoundInputArcs

    def addOutBoundInputArcs(self, newOutBoundInputArc):
        '''
        Setter function to add new outbound input arc originating from current Place, to Place's outbound Input Arc list.
        Note: this function adds one new Input Arc to the Place's outbound Input Arc list. To overwrite the list with a tuple of multiple Input Arcs, use setOutBoundInputArcs.
        @param newOutBoundInputArc: New Input Arc to be added to Place's outbound Input Arc list, must be instance of class Input Arc
        '''
        if(checkType(newOutBoundInputArc) != "InputArc"):
            raise Exception("Place's new outbound Input Arc must be instance of class Input Arc")
        newOutBoundInputArc.setFromPlace(self)
        self.outBoundInputArcs.append(newOutBoundInputArc)
    
    # INBOUND OUTPUT ARCS
    def setInBoundOutputArcs(self, *inBoundOutputArcList):
        '''
        Setter function to overwrite inbound output arcs targeting current Place.
        Note: this function deletes existing list of inbound output arcs, and creates new list with the given parameters. To add single new Output Arc to Place's inbound Output Arc list, use addInBoundOutputArcs.
        @param *inBoundOutputArcList: New tuple of Output Arcs to be added to Place's inbound Output Arc list, must be a tuple of instances of class Output Arc
        '''
        for arc in inBoundOutputArcList:
            if(checkType(arc) != "OutputArc"):
                raise Exception("Place's new inbound Output Arc list's elements must be instances of class Output Arc")
        self.inBoundOutputArcs.clear
        for arc in inBoundOutputArcList:
            arc.setToPlace(self)
            self.inBoundOutputArcs.append(arc)
    
    def getInBoundOutputArcs(self):
        '''
        Getter function for list of inbound output arcs targeting current Place.
        Returns current list of inbound output arcs targeting current Place.
        '''
        return self.inBoundOutputArcs

    def addInBoundOutputArcs(self, newInBoundOutputArc):
        '''
        Setter function to add new inbound output arc targeting current Place, to Place's inbound Output Arc list.
        Note: this function adds one new Output Arc to the Place's inbound Output Arc list. To overwrite the list with a tuple of multiple Output Arcs, use setInBoundOutputArcs.
        @param newInBoundOutputArc: New Output Arc to be added to Place's inbound Output Arc list, must be instance of class Output Arc
        '''
        if(checkType(newInBoundOutputArc) != "OutputArc"):
            raise Exception("Place's new inbound Output Arc must be instance of class Output Arc")
        newInBoundOutputArc.setToPlace(self)
        self.inBoundOutputArcs.append(newInBoundOutputArc)

    # OUTBOUND INHIB ARCS
    def setOutBoundInhibArcs(self, *outBoundInhibArcList):
        '''
        Setter function to overwrite outbound inhibitor arcs originating from current Place.
        Note: this function deletes existing list of outbound inhibitor arcs, and creates new list with the given parameters. To add single new Inhibitor Arc to Place's outbound Inhibitor Arc list, use addOutBoundInhibArcs.
        @param *outBoundInhibArcList: New tuple of Inhibitor Arcs to be added to Place's outbound Inhibitor Arc list, must be a tuple of instances of class Inhibitor Arc
        '''
        for arc in outBoundInhibArcList:
            if(checkType(arc) != "InhibArc"):
                raise Exception("Place's new outbound Inhibitor Arc list's elements must be instances of class Inhibitor Arc")
        self.outBoundInhibArcs.clear
        for arc in outBoundInhibArcList:
            arc.setOrigin(self)
            self.outBoundInhibArcs.append(arc)
    
    def getOutBoundInhibArcs(self):
        '''
        Getter function for list of outbound inhibitor arcs originating from current Place.
        Returns current list of outbound inhibitor arcs originating from current Place.
        '''
        return self.outBoundInhibArcs

    def addOutBoundInhibArcs(self, newOutBoundInhibArc):
        '''
        Setter function to add new outbound inhibitor arc originating from current Place, to Place's outbound Inhibitor Arc list.
        Note: this function adds one new Inhibitor Arc to the Place's outbound Inhibitor Arc list. To overwrite the list with a tuple of multiple Inhibitor Arcs, use setOutBoundInhibArcs.
        @param newOutBoundInhibArc: New Inhibitor Arc to be added to Place's outbound Inhibitor Arc list, must be instance of class Inhibitor Arc
        '''
        if(checkType(newOutBoundInhibArc) != "InhibArc"):
            raise Exception("Place's new outbound Inhibitor Arc must be instance of class Inhibitor Arc")
        newOutBoundInhibArc.setOrigin(self)
        self.outBoundInhibArcs.append(newOutBoundInhibArc)

    # INBOUND INHIB ARCS
    def setInBoundInhibArcs(self, *inBoundInhibArcList):
        '''
        Setter function to overwrite inbound inhibitor arcs targeting current Place.
        Note: this function deletes existing list of inbound inhibitor arcs, and creates new list with the given parameters. To add single new Inhibitor Arc to Place's inbound Inhibitor Arc list, use addInBoundInhibArcs.
        @param *inBoundInhibArcList: New tuple of Inhibitor Arcs to be added to Place's inbound Inhibitor Arc list, must be a tuple of instances of class Inhibitor Arc
        '''
        for arc in inBoundInhibArcList:
            if(checkType(arc) != "InhibArc"):
                raise Exception("Place's new inbound Inhibitor Arc list's elements must be instances of class Inhibitor Arc")
        self.inBoundInhibArcs.clear
        for arc in inBoundInhibArcList:
            arc.setTarget(self)
            self.inBoundInhibArcs.append(arc)
    
    def getInBoundInhibArcs(self):
        '''
        Getter function for list of inbound inhibitor arcs targeting current Place.
        Returns current list of inbound inhibitor arcs targeting current Place.
        '''
        return self.inBoundInhibArcs

    def addInBoundInhibArcs(self, newInBoundInhibArc):
        '''
        Setter function to add new inbound inhibitor arc targeting current Place, to Place's inbound Inhibitor Arc list.
        Note: this function adds one new Inhibitor Arc to the Place's inbound Inhibitor Arc list. To overwrite the list with a tuple of multiple Inhibitor Arcs, use setInBoundInhibArcs.
        @param newInBoundInhibArc: New Inhibitor Arc to be added to Place's inbound Inhibitor Arc list, must be instance of class Inhibitor Arc
        '''
        if(checkType(newInBoundInhibArc) != "InhibArc"):
            raise Exception("Place's new inbound Inhibitor Arc must be instance of class Inhibitor Arc")
        newInBoundInhibArc.setTarget(self)
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

def checkType(object):
    return object.__class__.__name__


# # NAME
# def setName(placeName: str, newName: str):
#     place = findPlaceByName(placeName)
#     if (checkName(newName)):
#         place.name = newName
#     else:
#         raise Exception("A Place already exists named: " + newName)

# def getName(placeName: str):
#     place = findPlaceByName(placeName)
#     return place.name
    
# # START
# def setStart(placeName: str, start: bool):
#     place = findPlaceByName(placeName)
#     place.start = start

# def getStart(placeName: str):
#     place = findPlaceByName(placeName)
#     return place.start

# # TOKENS
# def setTokens(placeName: str, tokens: int):
#     place = findPlaceByName(placeName)
#     place.tokens = tokens

# def getTokens(placeName: str):
#     place = findPlaceByName(placeName)
#     return place.tokens
    
# # TOTAL TOKENS
# def setTotalTokens(placeName: str, totalTokens: int):
#     place = findPlaceByName(placeName)
#     place.totalTokens = totalTokens

# def getTotalTokens(placeName: str):
#     place = findPlaceByName(placeName)
#     return place.totalTokens

# # MAX TOKENS
# def setMaxTokens(placeName: str, maxTokens: int):
#     place = findPlaceByName(placeName)
#     place.maxTokens = maxTokens

# def getMaxTokens(placeName: str):
#     place = findPlaceByName(placeName)
#     return place.maxTokens

# # OUTBOUND INPUT ARCS
# def setOutBoundInputArcs(placeName: str, *outBoundInputArcList):
#     place = findPlaceByName(placeName)
#     place.outBoundInputArcs.clear
#     for arc in outBoundInputArcList:
#         place.outBoundInputArcs.append(arc)
    
# def getOutBoundInputArcs(placeName: str):
#     place = findPlaceByName(placeName)
#     return place.outBoundInputArcs

# def addOutBoundInputArcs(placeName: str, newOutBoundInputArc):
#     place = findPlaceByName(placeName)
#     place.outBoundInputArcs.append(newOutBoundInputArc)

# # INBOUND OUTPUT ARCS
# def setInBoundOutputArcs(placeName: str, *inBoundOutputArcList):
#     place = findPlaceByName(placeName)
#     place.inBoundOutputArcs.clear
#     for arc in inBoundOutputArcList:
#         place.inBoundOutputArcs.append(arc)
    
# def getInBoundOutputArcs(placeName: str):
#     place = findPlaceByName(placeName)
#     return place.inBoundOutputArcs

# def addInBoundOutputArcs(placeName: str, newInBoundOutputArc):
#     place = findPlaceByName(placeName)
#     place.inBoundOutputArcs.append(newInBoundOutputArc)

# # OUTBOUND INHIB ARCS
# def setOutBoundInhibArcs(placeName: str, *outBoundInhibArcList):
#     place = findPlaceByName(placeName)
#     place.outBoundInhibArcs.clear
#     for arc in outBoundInhibArcList:
#         place.outBoundInhibArcs.append(arc)
    
# def getOutBoundInhibArcs(placeName: str):
#     place = findPlaceByName(placeName)
#     return place.outBoundInhibArcs

# def addOutBoundInhibArcs(placeName: str, newOutBoundInhibArc):
#     place = findPlaceByName(placeName)
#     place.outBoundInhibArcs.append(newOutBoundInhibArc)

# # INBOUND INHIB ARCS
# def setInBoundInhibArcs(placeName: str, *inBoundInhibArcList):
#     place = findPlaceByName(placeName)
#     place.inBoundInhibArcs.clear
#     for arc in inBoundInhibArcList:
#         place.inBoundInhibArcs.append(arc)
    
# def getInBoundInhibArcs(placeName: str):
#     place = findPlaceByName(placeName)
#     return place.inBoundInhibArcs

# def addInBoundInhibArcs(placeName: str, newInBoundInhibArc):
#     place = findPlaceByName(placeName)
#     place.inBoundInhibArcs.append(newInBoundInhibArc)
