from main import outputEdgeList

class OutputArc:

    def __init__(self, name: str, fromTrans, toPlace, multiplicity: int = 1):
        '''
        Create an instance of the Output Arc class.
        @param name: Unique name of the Output Arc, must be string
        @param fromTrans: Origin transition of the Output Arc, must be instance of class Timed Transition or Instant Transition
        @param toPlace: Target palce of the Output Arc, must be instance of class Place
        @param multiplicity: Multiplicity of the Output Arc, must be integer
        '''
        if (checkName(name)):
            self.name = name                                                        # name of the arc, recommended format: {Origin trans name}{Target place name}Arc ie. WaitServiceArc

            if(checkType(fromTrans) == "TimedTransition"):                          # Adding reference of Output Arc to Origin Transition's outbound Output Arc list
                self.fromTrans = fromTrans                                          # reference of origin Transition TODO: might change it to name and perform search in transList
                fromTrans.addOutBoundOutputArcs(self)
            elif(checkType(fromTrans) == "InstantTransition"):
                self.fromTrans = fromTrans                                          # reference of origin Transition TODO: might change it to name and perform search in transList
                fromTrans.addOutBoundOutputArcs(self)
            else:
                del self
                raise Exception("Output arc's fromTrans parameter must be instance of class Timed Transition or Instant Transition")

            if(checkType(toPlace) == "Place"):                                      # Adding reference of Output Arc to Target Place's inbound Output Arc list
                self.toPlace = toPlace                                              # reference of target Place TODO: might change it to name and perform search in placeList
                toPlace.addInBoundOutputArcs(self)
            else:
                del self
                raise Exception("Output arc's toPlace parameter must be instance of class Place")

            self.multiplicity = multiplicity                                        # multiplicity of arc

            outputEdgeList.append(self)

        else:
            del self
            raise Exception("Output arc already exists named: " + name)

    def __str__(self):
        '''
        Default return value of class, gives description of current state of Output Arc.
        '''
        returnString = f'Output arc (name={self.name}, '                            # Print name of Output Arc
        if(checkType(self.fromTrans) == "TimedTransition"):      # Print name of origin Transition
            returnString += f'from Timed Transition={self.fromTrans.name}, '
        elif(checkType(self.fromTrans) == "InstantTransition"):
            returnString += f'from Immediate Transition={self.fromTrans.name}, '
        returnString += f'to Place={self.toPlace.name}, '                           # Print name of target Place
        returnString += f'multiplicity={self.multiplicity}'                         # Print multiplicity of Output arc

        return returnString

    # NAME
    def setName(self, newName: str):
        '''
        Setter function for name of Output Arc.
        @param newName: Unique new name for Output Arc, must be string
        '''
        if (checkName(newName)):
            self.name = newName
        else:
            raise Exception("An Output arc already exists named: " + newName)

    def getName(self):
        '''
        Getter function for name of Output arc.
        Returns current name of Output Arc.
        '''
        return self.name
    
    # FROM TRANS
    def setFromTrans(self, fromTrans):
        '''
        Setter function for origin transition of Output Arc.
        @param fromTrans: New origin place for Output Arc, must be instance of class Timed Transition or Instant Transition
        '''
        if(checkType(fromTrans) == "TimedTransition"):
            if self in self.fromTrans.outBoundOutputArcs:
                self.fromTrans.outBoundOutputArcs.remove(self)                        # remove reference to output arc from old origin timed transition's outbound Output Arc list
            fromTrans.addOutBoundOutputArcs(self)                                 # add reference to output arc to new origin timed transition's outbound Output Arc list
        elif(checkType(fromTrans) == "InstantTransition"):
            if self in self.fromTrans.outBoundOutputArcs:
                self.fromTrans.outBoundOutputArcs.remove(self)                        # remove reference to output arc from old origin instant transition's outbound Output Arc list
            fromTrans.addOutBoundOutputArcs(self)                                 # add reference to output arc to new origin instant transition's outbound Output Arc list
        else:
            raise Exception("Output arc's new origin transition parameter must be instance of class Timed Transition of Instant Transition")
        self.fromTrans = fromTrans

    def getFromTrans(self):
        '''
        Getter function for origin transition of Output arc.
        Returns current origin transition of Output Arc.
        '''
        return self.fromTrans

    # TO PLACE
    def setToPlace(self, toPlace):
        '''
        Setter function for target place of Output Arc.
        @param toPlace: New target place for Output Arc, must be instance of class Place
        '''
        if(checkType(toPlace) == "Place"):
            if self in self.toPlace.inBoundOutputArcs:
                self.toPlace.inBoundOutputArcs.remove(self)                         # remove reference to output arc from old target place's inbound Output Arc list
            toPlace.addInBoundOutputArcs(self)                                  # add reference to output arc to new target place's inbound Output Arc list
        else:
            raise Exception("Output arc's new target place parameter must be instance of class Place")
        self.toPlace = toPlace

    def getToPlace(self):
        '''
        Getter function for target place of Output arc.
        Returns current target place of Output Arc.
        '''
        return self.toPlace
    
    # MULTIPLICITY
    def setMultiplicity(self, multiplicity: int):
        '''
        Setter function for multiplicity of Output Arc.
        @param multiplicity: New multiplicity value for Output Arc, must be integer
        '''
        self.multiplicity = multiplicity

    def getMultiplicity(self):
        '''
        Getter function for multiplicity of Output Arc.
        Returns current multiplicity of Output Arc.
        '''
        return self.multiplicity


def checkName(name):
    for outputEdge in outputEdgeList:
        if (outputEdge.name == name):
            return False
    return True

def findOutputEdgeByName(name):
    for outputEdge in outputEdgeList:
        if (outputEdge.name == name):
            return outputEdge
    raise Exception('Output arc does not exists with name: ' + name)

def checkType(object):
    return object.__class__.__name__


# def setName(edgeName: str, newName: str):
#     outputEdge = findOutputEdgeByName(edgeName)
#     if (checkName(newName)):
#         outputEdge.name = newName
#     else:
#         raise Exception("An Output arc already exists named: " + newName)

# def getName(edgeName: str):
#     outputEdge = findOutputEdgeByName(edgeName)
#     return outputEdge.name
    
# def setFromTrans(edgeName: str, fromTrans: 'TimedTransition' | 'InstantTransition'):
#     outputEdge = findOutputEdgeByName(edgeName)
#     outputEdge.fromTrans = fromTrans

# def getFromTrans(edgeName: str):
#     outputEdge = findOutputEdgeByName(edgeName)
#     return outputEdge.fromTrans

# def setToPlace(edgeName: str, toPlace: 'Place'):
#     outputEdge = findOutputEdgeByName(edgeName)
#     outputEdge.toPlace = toPlace

# def getToPlace(edgeName: str):
#     outputEdge = findOutputEdgeByName(edgeName)
#     return outputEdge.toPlace
    
# def setMultiplicity(edgeName: str, multiplicity: int):
#     outputEdge = findOutputEdgeByName(edgeName)
#     outputEdge.multiplicity = multiplicity

# def getMultiplicity(edgeName: str):
#     outputEdge = findOutputEdgeByName(edgeName)
#     return outputEdge.multiplicity