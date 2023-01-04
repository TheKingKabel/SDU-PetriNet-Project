from main import outputEdgeList
import place
import timedTransition
import instantTransition

class OutputArc:

    def __init__(self, name: str, fromTrans: timedTransition.TimedTransition | instantTransition.InstantTransition, toPlace: place.Place, multiplicity: int = 1):
        if (checkName(name)):
            self.name = name #name of the arc, recommended format: {Origin trans name}{Target place name}Arc ie. WaitServiceArc
            self.fromTrans = fromTrans #reference of origin Transition TODO: might change it to name and perform search in transList
            self.toPlace = toPlace #reference of target Place TODO: might change it to name and perform search in placeList
            self.multiplicity = multiplicity #multiplicity of arc

            outputEdgeList.append(self)

        else:
            del self
            raise Exception("Output arc already exists named: " + name)

    def __str__(self):
        return f'Output arc (name={self.name}, from Transition={self.fromTrans.name}, to Place={self.toPlace.name}, multiplicity={self.multiplicity}'

    def setName(self, newName: str):
        if (checkName(newName)):
            self.name = newName
        else:
            raise Exception("An Output arc already exists named: " + newName)

    def getName(self):
        return self.name
    
    def setFromTrans(self, fromTrans: timedTransition.TimedTransition | instantTransition.InstantTransition):
        self.fromTrans = fromTrans

    def getFromTrans(self):
        return self.fromTrans

    def setToPlace(self, toPlace: place.Place):
        self.toPlace = toPlace

    def getToPlace(self):
        return self.toPlace
    
    def setMultiplicity(self, multiplicity: int):
        self.multiplicity = multiplicity

    def getMultiplicity(self):
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


def setName(edgeName: str, newName: str):
    outputEdge = findOutputEdgeByName(edgeName)
    if (checkName(newName)):
        outputEdge.name = newName
    else:
        raise Exception("An Output arc already exists named: " + newName)

def getName(edgeName: str):
    outputEdge = findOutputEdgeByName(edgeName)
    return outputEdge.name
    
def setFromTrans(edgeName: str, fromTrans: timedTransition.TimedTransition | instantTransition.InstantTransition):
    outputEdge = findOutputEdgeByName(edgeName)
    outputEdge.fromTrans = fromTrans

def getFromTrans(edgeName: str):
    outputEdge = findOutputEdgeByName(edgeName)
    return outputEdge.fromTrans

def setToPlace(edgeName: str, toPlace: place.Place):
    outputEdge = findOutputEdgeByName(edgeName)
    outputEdge.toPlace = toPlace

def getToPlace(edgeName: str):
    outputEdge = findOutputEdgeByName(edgeName)
    return outputEdge.toPlace
    
def setMultiplicity(edgeName: str, multiplicity: int):
    outputEdge = findOutputEdgeByName(edgeName)
    outputEdge.multiplicity = multiplicity

def getMultiplicity(edgeName: str):
    outputEdge = findOutputEdgeByName(edgeName)
    return outputEdge.multiplicity