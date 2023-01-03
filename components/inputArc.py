from main import inputEdgeList
import transition

class InputArc:

    def __init__(self, name: str, fromPlace: place.Place, toTrans: transition.Transition, multiplicity: int = 1):
        if (checkName(name)):
            self.name = name #name of the arc, recommended format: {Origin place name}{Target transition name}Arc ie. QueueWaitArc
            self.fromPlace = fromPlace #reference of origin Place TODO: might change it to name and perform search in placeList
            self.toTrans = toTrans #reference of target Transition TODO: might change it to name and perform search in transList
            self.multiplicity = multiplicity #multiplicity of arc

            inputEdgeList.append(self)

        else:
            del self
            raise Exception("Input arc already exists named: " + name)

    def __str__(self):
        return f'Input arc (name={self.name}, from Place={self.fromPlace.name}, to Transition={self.toTrans.name}, multiplicity={self.multiplicity}'

    def setName(self, newName: str):
        if (checkName(newName)):
            self.name = newName
        else:
            raise Exception("An Input arc already exists named: " + newName)

    def getName(self):
        return self.name
    
    def setFromPlace(self, fromPlace: place.Place):
        self.fromPlace = fromPlace

    def getFromPlace(self):
        return self.fromPlace

    def setToTrans(self, toTrans: transition.Transition):
        self.toTrans = toTrans

    def getToTrans(self):
        return self.toTrans
    
    def setMultiplicity(self, multiplicity: int):
        self.multiplicity = multiplicity

    def getMultiplicity(self):
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


def setName(edgeName: str, newName: str):
    inputEdge = findInputEdgeByName(edgeName)
    if (checkName(newName)):
        inputEdge.name = newName
    else:
        raise Exception("An Input arc already exists named: " + newName)

def getName(edgeName: str):
    inputEdge = findInputEdgeByName(edgeName)
    return inputEdge.name
    
def setFromPlace(edgeName: str, fromPlace: place.Place):
    inputEdge = findInputEdgeByName(edgeName)
    inputEdge.fromPlace = fromPlace

def getFromPlace(edgeName: str):
    inputEdge = findInputEdgeByName(edgeName)
    return inputEdge.fromPlace

def setTokens(edgeName: str, toTrans: transition.Transition):
    inputEdge = findInputEdgeByName(edgeName)
    inputEdge.toTrans = toTrans

def getTokens(edgeName: str):
    inputEdge = findInputEdgeByName(edgeName)
    return inputEdge.tokens
    
def setMultiplicity(edgeName: str, multiplicity: int):
    inputEdge = findInputEdgeByName(edgeName)
    inputEdge.multiplicity = multiplicity

def getMultiplicity(edgeName: str):
    inputEdge = findInputEdgeByName(edgeName)
    return inputEdge.multiplicity

import place