from main import inhibList


class InhibArc:

    def __init__(self, name: str, origin, target, multiplicity: int = 1):
        '''
        Create an instance of the Inhibitor Arc class.
        @param name: Unique name of the Inhibitor Arc, must be string
        @param origin: Origin element of the Inhibitor Arc, must be instance of class Timed Transition, Immediate Transition or Place
        @param target: Target element of the Inhibitor Arc, must be instance of class Timed Transition, Immediate Transition or Place
        @param multiplicity: Multiplicity of the Inhibitor Arc, must be integer
        '''
        if (checkName(name)):
            # name of the Arc, recommended format: {Origin name}{Target name}InhibArc ie. WaitServiceInhibArc
            self.name = name

            # Adding reference of Inhibitor Arc to Origin's Inhibitor Arc list
            if(checkType(origin) == "Place"):
                # reference of origin Place TODO: might change it to name and perform search in lists
                self.origin = origin
                origin.addInhibArcs(self)
            else:
                del self
                raise Exception(
                    "Inhibitor Arc's origin parameter must be instance of class Place")

            if(checkType(target) == "TimedTransition"):
                # reference of target Transition TODO: might change it to name and perform search in lists
                self.target = target
                target.addInhibArcs(self)
            elif(checkType(target) == "ImmediateTransition"):
                # reference of target Transition TODO: might change it to name and perform search in lists
                self.target = target
                target.addInhibArcs(self)
            else:
                del self
                raise Exception(
                    "Inhibitor Arc's target parameter must be instance of class Timed Transition or Immediate Transition")

            # multiplicity of Arc
            self.multiplicity = multiplicity

            # append to list of current PN net of inhibitors
            inhibList.append(self)

        else:
            del self
            raise Exception("Inhibitor Arc already exists named: " + name)

    def __str__(self):
        '''
        Default return value of class, gives description of current state of Inhibitor.
        '''
        returnString = f'Inhibitor Arc (name={self.name}, '
        returnString += f'from Place={self.origin.name}, '
        if(checkType(self.target) == "TimedTransition"):
            returnString += f'to Timed Transition={self.target.name}, '
        elif(checkType(self.target) == "ImmediateTransition"):
            returnString += f'to Immediate Transition={self.target.name}, '
        returnString += f'multiplicity={self.multiplicity}'

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
            raise Exception(
                "An Inhibitor Arc already exists named: " + newName)

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
        @param newOrigin: New origin for Inhibitor, must be instance of class Timed Transition, Immediate Transition or Place
        '''
        if(checkType(newOrigin) == "Place"):
            if self in self.origin.inhibArcs:
                # remove reference to Inhibitor Arc from old origin Place's Inhibitor Arc list
                self.origin.inhibArcs.remove(self)
            # add reference to Inhibitor Arc to new origin Place's Inhibitor Arc list
            newOrigin.addInhibArcs(self)
        else:
            raise Exception(
                "Inhibitor Arc's new origin parameter must be instance of class Place")
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
        @param newTarget: New target for Inhibitor, must be instance of class Timed Transition or Immediate Transition
        '''
        if(checkType(newTarget) == "TimedTransition"):
            if self in self.target.inhibArcs:
                # remove reference to Inhibitor Arc from old target Transition's Inhibitor Arc list
                self.target.inhibArcs.remove(self)
            # add reference to Inhibitor Arc to new target Transition's Inhibitor Arc list
            newTarget.addInhibArcs(self)
        elif(checkType(newTarget) == "ImmediateTransition"):
            if self in self.target.inhibArcs:
                self.target.inhibArcs.remove(self)
            newTarget.addInhibArcs(self)
        else:
            raise Exception(
                "Inhibitor Arc's new target parameter must be instance of class Timed Transition or Immediate Transition")
        self.target = newTarget

    def getTarget(self):
        '''
        Getter function for target of Inhibitor.
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
    raise Exception('Inhibitor Arc does not exists with name: ' + name)


def checkType(object):
    return object.__class__.__name__
