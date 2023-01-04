from main import inhibList
import place
import timedTransition
import instantTransition

class InhibArc:

    def __init__(self, name: str, origin: timedTransition.TimedTransition | place.Place | instantTransition.InstantTransition, target: timedTransition.TimedTransition | place.Place | instantTransition.InstantTransition, multiplicity: int = 1):
        if (checkName(name)):
            self.name = name                    # name of the arc, recommended format: {Origin trans/place name}{Target trans/place name}Arc ie. WaitServiceArc
            if(isinstance(origin, place.Place)):      # TODO: make similar for transition
                origin.addOutBoundInhibArcs(self)
            self.origin = origin                # reference of origin Transition or Place TODO: might change it to name and perform search in lists
            if(isinstance(target, place.Place)):       # TODO: make similar for transition
                target.addInBoundInhibArcs(self)
            self.target = target                # reference of target Transition or Place TODO: might change it to name and perform search in lists
            self.multiplicity = multiplicity    # multiplicity of arc

            inhibList.append(self)

        else:
            del self
            raise Exception("Inhibitor arc already exists named: " + name)

    def __str__(self):
        returnString = f'Inhibitor arc (name={self.name}, '
        if(isinstance(self.origin, timedTransition.TimedTransition | instantTransition.InstantTransition)):
            returnString += f'from Transition={self.origin.name}, '
        elif(isinstance(self.origin, place.Place)):
            returnString += f'from Place={self.origin.name}, '
        
        if(isinstance(self.target, timedTransition.TimedTransition | instantTransition.InstantTransition)):
            returnString += f'to Transition={self.target.name}, '
        elif(isinstance(self.target, place.Place)):
            returnString += f'from Place={self.target.name}, '

        returnString += f'multiplicity={self.multiplicity}'

        return returnString

    def setName(self, newName: str):
        if (checkName(newName)):
            self.name = newName
        else:
            raise Exception("An Inhibitor arc already exists named: " + newName)

    def getName(self):
        return self.name

    def setMultiplicity(self, multiplicity: int):
        self.multiplicity = multiplicity
    
    def getMultiplicity(self):
        return self.multiplicity
    

    def setOrigin(self, newOrigin: timedTransition.TimedTransition | place.Place | instantTransition.InstantTransition):
        self.origin.outBoundInhibArcs.remove(self)  # remove reference to inhibitor from old origin's outbound inhibitor list
        if(isinstance(newOrigin, place.Place)):            # TODO: make similar to transition
            newOrigin.addOutBoundInhibArcs(self)
        self.origin = newOrigin

    def getOrigin(self):
        return self.origin

    def setTarget(self, newTarget: timedTransition.TimedTransition | place.Place | instantTransition.InstantTransition):
        self.target.inBoundInhibArcs.remove(self)  # remove reference to inhibitor from old target's inbound inhibitor list
        if(isinstance(newTarget, place.Place)):           # TODO: make similar to transition
            newTarget.addInBoundInhibArcs(self)
        self.target = newTarget

    def getTarget(self):
        return self.target



def checkName(name):
    for inhibEdge in inhibList:
        if (inhibEdge.name == name):
            return False
    return True

def findInhibEdgeByName(name):
    for inhibEdge in inhibList:
        if (inhibEdge.name == name):
            return inhibEdge
    raise Exception('Inhibitor arc does not exists with name: ' + name)


def setName(edgeName: str, newName: str):
    inhibEdge = findInhibEdgeByName(edgeName)
    if (checkName(newName)):
        inhibEdge.name = newName
    else:
        raise Exception("An Inhibitor arc already exists named: " + newName)
    
def getName(edgeName: str):
    inhibEdge = findInhibEdgeByName(edgeName)
    return inhibEdge.name
    
def setMultiplicity(edgeName: str, multiplicity: int):
    inhibEdge = findInhibEdgeByName(edgeName)
    inhibEdge.multiplicity = multiplicity

def getMultiplicity(edgeName: str):
    inhibEdge = findInhibEdgeByName(edgeName)
    return inhibEdge.multiplicity

def setOrigin(edgeName: str, newOrigin: timedTransition.TimedTransition | place.Place | instantTransition.InstantTransition):
    inhibEdge = findInhibEdgeByName(edgeName)
    if(isinstance(newOrigin, place.Place)):            # TODO: make similar to transition
        newOrigin.addOutBoundInhibArcs(inhibEdge)
    inhibEdge.origin = newOrigin

def getOrigin(edgeName: str):
    inhibEdge = findInhibEdgeByName(edgeName)
    return inhibEdge.origin

def setTarget(edgeName: str, newTarget: timedTransition.TimedTransition | place.Place | instantTransition.InstantTransition):
    inhibEdge = findInhibEdgeByName(edgeName)
    if(isinstance(newTarget, place.Place)):            # TODO: make similar to transition
        newTarget.addOutBoundInhibArcs(inhibEdge)
    inhibEdge.target = newTarget

def getTarget(edgeName: str):
    inhibEdge = findInhibEdgeByName(edgeName)
    return inhibEdge.target