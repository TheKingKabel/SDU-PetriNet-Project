from main import inputEdgeList

class InputArc:

    def __init__(self, name: str, fromPlace, toTrans, multiplicity: int = 1):
        '''
        Create an instance of the Input Arc class.
        @param name: Unique name of the Input Arc, must be string
        @param fromPlace: Origin place of the Input Arc, must be instance of class Place
        @param toTrans: Target transition of the Input Arc, must be instance of class Timed Transition or Instant Transition
        @param multiplicity: Multiplicity of the Input Arc, must be integer
        '''
        if (checkName(name)):
            self.name = name                                                    # name of the arc, recommended format: {Origin name}{Target name}Arc ie. WaitServiceArc
            
            if(checkType(fromPlace) == "Place"):                                # Adding reference of Input Arc to Origin's outbound Input Arc list
                self.fromPlace = fromPlace                                      # reference of origin Place TODO: might change it to name and perform search in placeList
                fromPlace.addOutBoundInputArcs(self)
            else:
                del self
                raise Exception("Input arc's fromPlace parameter must be instance of class Place")
            
            if(checkType(toTrans) == "TimedTransition"):     # Adding reference of Input Arc to Target's inbound Input Arc list
                self.toTrans = toTrans
                toTrans.addInBoundInputArcs(self)
            elif(checkType(toTrans) == "InstantTransition"):
                self.toTrans = toTrans
                toTrans.addInBoundInputArcs(self)
            else:
                del self
                raise Exception("Input arc's toTrans parameter must be instance of class Timed Transition or Instant Transition")
            
            self.multiplicity = multiplicity                                    # multiplicity of arc

            inputEdgeList.append(self)                                          # append to list of current PN net of input arcs

        else:
            del self
            raise Exception("Input arc already exists named: " + name)

    def __str__(self):
        '''
        Default return value of class, gives description of current state of Input Arc.
        '''
        returnString = f'Input arc (name={self.name}, '                         # Print name of Input Arc
        returnString += f'from Place={self.fromPlace.name}, '                   # Print name of origin Place
        if(checkType(self.toTrans) == "TimedTransition"):    # Print name of target Transition
            returnString += f'to Timed Transition={self.toTrans.name}, '
        elif(checkType(self.toTrans) == "InstantTransition"):
            returnString += f'to Immediate Transition={self.toTrans.name}, '
        returnString += f'multiplicity={self.multiplicity}'                     # Print multiplicity of Input arc

        return returnString

    # NAME
    def setName(self, newName: str):
        '''
        Setter function for name of Input Arc.
        @param newName: Unique new name for Input Arc, must be string
        '''
        if (checkName(newName)):
            self.name = newName
        else:
            raise Exception("An Input arc already exists named: " + newName)

    def getName(self):
        '''
        Getter function for name of Input arc.
        Returns current name of Input Arc.
        '''
        return self.name
    
    # FROM PLACE
    def setFromPlace(self, fromPlace):
        '''
        Setter function for origin place of Input Arc.
        @param fromPlace: New origin place for Input Arc, must be instance of class Place
        '''
        if(checkType(fromPlace) == "Place"):
            if self in self.fromPlace.outBoundInputArcs:
                self.fromPlace.outBoundInputArcs.remove(self)                     # remove reference to input arc from old origin place's outbound Input Arc list
            fromPlace.addOutBoundInputArcs(self)                              # add reference to input arc to new origin place's outbound Input Arc list
        else:
            raise Exception("Input arc's new origin place parameter must be instance of class Place")
        self.fromPlace = fromPlace

    def getFromPlace(self):
        '''
        Getter function for origin place of Input arc.
        Returns current origin place of Input Arc.
        '''
        return self.fromPlace

    # TO TRANS
    def setToTrans(self, toTrans):
        '''
        Setter function for target transition of Input Arc.
        @param toTrans: New target transition for Input Arc, must be instance of class Timed Transition of Instant Transition
        '''
        if(checkType(toTrans) == "TimedTransition"):
            if self in self.toTrans.inBoundInputArcs:
                self.toTrans.inBoundInputArcs.remove(self)                        # remove reference to input arc from old target timed transition's inbound Input Arc list
            toTrans.addInBoundInputArcs(self)                                 # add reference to input arc to new target timed transition's inbound Input Arc list
        elif(checkType(toTrans) == "InstantTransition"):
            if self in self.toTrans.inBoundInputArcs:
                self.toTrans.inBoundInputArcs.remove(self)                        # remove reference to input arc from old target instant transition's inbound Input Arc list
            toTrans.addInBoundInputArcs(self)                                 # add reference to input arc to new target instant transition's inbound Input Arc list
        else:
            raise Exception("Input arc's new target transition parameter must be instance of class Timed Transition of Instant Transition")
        self.toTrans = toTrans

    def getToTrans(self):
        '''
        Getter function for target transition of Input arc.
        Returns current target transition of Input Arc.
        '''
        return self.toTrans
    
    # MULTIPLICITY
    def setMultiplicity(self, multiplicity: int):
        '''
        Setter function for multiplicity of Input Arc.
        @param multiplicity: New multiplicity value for Input Arc, must be integer
        '''
        self.multiplicity = multiplicity

    def getMultiplicity(self):
        '''
        Getter function for multiplicity of Input Arc.
        Returns current multiplicity of Input Arc.
        '''
        return self.multiplicity


def checkName(name):
    for inputEdge in inputEdgeList:
        if (inputEdge.name == name):
            return False
    return True

def findInputEdgeByName(name):
    for inputEdge in inputEdgeList:
        if (inputEdge.name == name):
            return inputEdge
    raise Exception('Input arc does not exists with name: ' + name)

def checkType(object):
    return object.__class__.__name__


# def setName(edgeName: str, newName: str):
#     inputEdge = findInputEdgeByName(edgeName)
#     if (checkName(newName)):
#         inputEdge.name = newName
#     else:
#         raise Exception("An Input arc already exists named: " + newName)

# def getName(edgeName: str):
#     inputEdge = findInputEdgeByName(edgeName)
#     return inputEdge.name
    
# def setFromPlace(edgeName: str, fromPlace: 'Place'):
#     inputEdge = findInputEdgeByName(edgeName)
#     inputEdge.fromPlace = fromPlace

# def getFromPlace(edgeName: str):
#     inputEdge = findInputEdgeByName(edgeName)
#     return inputEdge.fromPlace

# def setTokens(edgeName: str, toTrans: 'TimedTransition' | 'InstantTransition'):
#     inputEdge = findInputEdgeByName(edgeName)
#     inputEdge.toTrans = toTrans

# def getTokens(edgeName: str):
#     inputEdge = findInputEdgeByName(edgeName)
#     return inputEdge.tokens
    
# def setMultiplicity(edgeName: str, multiplicity: int):
#     inputEdge = findInputEdgeByName(edgeName)
#     inputEdge.multiplicity = multiplicity

# def getMultiplicity(edgeName: str):
#     inputEdge = findInputEdgeByName(edgeName)
#     return inputEdge.multiplicity