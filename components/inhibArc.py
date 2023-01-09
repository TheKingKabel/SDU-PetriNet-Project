from main import inhibList

class InhibArc:

    def __init__(self, name: str, origin, target, multiplicity: int = 1):
        '''
        Create an instance of the Inhibitor Arc class.
        @param name: Unique name of the Inhibitor Arc, must be string
        @param origin: Origin element of the Inhibitor Arc, must be instance of class Timed Transition, Instant Transition or Place
        @param target: Target element of the Inhibitor Arc, must be instance of class Timed Transition, Instant Transition or Place
        @param multiplicity: Multiplicity of the Inhibitor Arc, must be integer
        '''
        if (checkName(name)):
            self.name = name                                 # name of the arc, recommended format: {Origin name}{Target name}InhibArc ie. WaitServiceInhibArc
            
            if(checkType(origin) == "Place"):                # Adding reference of Inhibitor Arc to Origin's outbound Inhibitor list
                self.origin = origin                         # reference of origin Transition or Place TODO: might change it to name and perform search in lists
                origin.addOutBoundInhibArcs(self)
            elif(checkType(origin) == "TimedTransition"):
                self.origin = origin                         # reference of origin Transition or Place TODO: might change it to name and perform search in lists
                origin.addOutBoundInhibArcs(self)
            elif(checkType(origin) == "InstantTransition"):
                self.origin = origin                         # reference of origin Transition or Place TODO: might change it to name and perform search in lists
                origin.addOutBoundInhibArcs(self)
            else:
                del self
                raise Exception("Inhibitor arc's origin parameter must be instance of class Place, Timed Transition or Instant Transition")
            
            if(checkType(target) == "Place"):                # Adding reference of Inhibitor Arc to Target's inbound Inhibitor list
                self.target = target                         # reference of target Transition or Place TODO: might change it to name and perform search in lists
                target.addInBoundInhibArcs(self)
            elif(checkType(target) == "TimedTransition"):
                self.target = target                         # reference of target Transition or Place TODO: might change it to name and perform search in lists
                target.addInBoundInhibArcs(self)
            elif(checkType(target) == "InstantTransition"):
                self.target = target                         # reference of target Transition or Place TODO: might change it to name and perform search in lists
                target.addInBoundInhibArcs(self)
            else:
                del self
                raise Exception("Inhibitor arc's target parameter must be instance of class Place, Timed Transition or Instant Transition")
            
            self.multiplicity = multiplicity                                    # multiplicity of arc

            inhibList.append(self)                                              # append to list of current PN net of inhibitors

        else:
            del self
            raise Exception("Inhibitor arc already exists named: " + name)

    def __str__(self):
        '''
        Default return value of class, gives description of current state of Inhibitor.
        '''
        returnString = f'Inhibitor arc (name={self.name}, '                     # Print name of Inhibitor
        
        if(checkType(self.origin) == "Place"):               # Print name of origin element
            returnString += f'from Place={self.origin.name}, '
        elif(checkType(self.origin) == "TimedTransition"):
            returnString += f'from Timed Transition={self.origin.name}, '
        elif(checkType(self.origin) == "InstantTransition"):
            returnString += f'from Immediate Transition={self.origin.name}, '
        
        if(checkType(self.target) == "Place"):               # Print name of target element
            returnString += f'to Place={self.target.name}, '
        elif(checkType(self.target) == "TimedTransition"):
            returnString += f'to Timed Transition={self.target.name}, '
        elif(checkType(self.target) == "InstantTransition"):
            returnString += f'to Immediate Transition={self.target.name}, '

        returnString += f'multiplicity={self.multiplicity}'                     # Print multiplicity of Inhibitor

        return returnString

    # NAME
    def setName(self, newName: str):
        '''
        Setter function for name of Inhibitor.
        @param newName: Unique new name for Inhibitor, must be string
        '''
        if (checkName(newName)):
            self.name = newName
        else:
            raise Exception("An Inhibitor arc already exists named: " + newName)

    def getName(self):
        '''
        Getter function for name of Inhibitor.
        Returns current name of Inhibitor.
        '''
        return self.name

    # MULTIPLICITY
    def setMultiplicity(self, multiplicity: int):
        '''
        Setter function for multiplicity of Inhibitor.
        @param multiplicity: New multiplicity value for Inhibitor, must be integer
        '''
        self.multiplicity = multiplicity
    
    def getMultiplicity(self):
        '''
        Getter function for multiplicity of Inhibitor.
        Returns current multiplicity of Inhibitor.
        '''
        return self.multiplicity
    
    # ORIGIN
    def setOrigin(self, newOrigin):
        '''
        Setter function for origin of Inhibitor.
        @param newOrigin: New origin for Inhibitor, must be instance of class Timed Transition, Instant Transition or Place
        '''
        if(checkType(newOrigin) == "Place"):               # Print name of origin element
            if self in self.origin.outBoundInhibArcs:   
                self.origin.outBoundInhibArcs.remove(self)                        # remove reference to inhibitor from old origin's outbound inhibitor list
            newOrigin.addOutBoundInhibArcs(self)                              # add reference to inhibitor to new origin's outbound inhibitor list
        elif(checkType(newOrigin) == "TimedTransition"):
            if self in self.origin.outBoundInhibArcs:   
                self.origin.outBoundInhibArcs.remove(self)
            newOrigin.addOutBoundInhibArcs(self)
        elif(checkType(newOrigin) == "InstantTransition"):
            if self in self.origin.outBoundInhibArcs:
                self.origin.outBoundInhibArcs.remove(self)
            newOrigin.addOutBoundInhibArcs(self)
        else:
            raise Exception("Inhibitor arc's new origin parameter must be instance of class Place, Timed Transition or Instant Transition")
        self.origin = newOrigin

    def getOrigin(self):
        '''
        Getter function for origin of Inhibitor.
        Returns current origin of Inhibitor.
        '''
        return self.origin

    # TARGET
    def setTarget(self, newTarget):
        '''
        Setter function for target of Inhibitor.
        @param newTarget: New target for Inhibitor, must be instance of class Timed Transition, Instant Transition or Place
        '''
        if(checkType(newTarget) == "Place"):              # Print name of target element
            if self in self.target.inBoundInhibArcs:
                self.target.inBoundInhibArcs.remove(self)                        # remove reference to inhibitor from old target's inbound inhibitor list
            newTarget.addInBoundInhibArcs(self)                              # add reference to inhibitor to new target's inbound inhibitor list
        elif(checkType(newTarget) == "TimedTransition"):
            if self in self.target.inBoundInhibArcs:
                self.target.inBoundInhibArcs.remove(self)
            newTarget.addInBoundInhibArcs(self)
        elif(checkType(newTarget) == "InstantTransition"):
            if self in self.target.inBoundInhibArcs:
                self.target.inBoundInhibArcs.remove(self)
            newTarget.addInBoundInhibArcs(self)
        else:
            raise Exception("Inhibitor arc's new target parameter must be instance of class Place, Timed Transition or Instant Transition")
        self.target = newTarget

    def getTarget(self):
        '''
        Getter function for targer of Inhibitor.
        Returns current target of Inhibitor.
        '''
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

def checkType(object):
    return object.__class__.__name__


# def setName(edgeName: str, newName: str):
#     inhibEdge = findInhibEdgeByName(edgeName)
#     if (checkName(newName)):
#         inhibEdge.name = newName
#     else:
#         raise Exception("An Inhibitor arc already exists named: " + newName)
    
# def getName(edgeName: str):
#     inhibEdge = findInhibEdgeByName(edgeName)
#     return inhibEdge.name
    
# def setMultiplicity(edgeName: str, multiplicity: int):
#     inhibEdge = findInhibEdgeByName(edgeName)
#     inhibEdge.multiplicity = multiplicity

# def getMultiplicity(edgeName: str):
#     inhibEdge = findInhibEdgeByName(edgeName)
#     return inhibEdge.multiplicity

# def setOrigin(edgeName: str, newOrigin: 'TimedTransition' | 'Place' | 'InstantTransition'):
#     inhibEdge = findInhibEdgeByName(edgeName)
#     if(isinstance(newOrigin, 'Place')):            # TODO: make similar to transition
#         newOrigin.addOutBoundInhibArcs(inhibEdge)
#     inhibEdge.origin = newOrigin

# def getOrigin(edgeName: str):
#     inhibEdge = findInhibEdgeByName(edgeName)
#     return inhibEdge.origin

# def setTarget(edgeName: str, newTarget: 'TimedTransition' | 'Place' | 'InstantTransition'):
#     inhibEdge = findInhibEdgeByName(edgeName)
#     if(isinstance(newTarget, place.Place)):            # TODO: make similar to transition
#         newTarget.addOutBoundInhibArcs(inhibEdge)
#     inhibEdge.target = newTarget

# def getTarget(edgeName: str):
#     inhibEdge = findInhibEdgeByName(edgeName)
#     return inhibEdge.target