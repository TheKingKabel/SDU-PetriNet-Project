
class InhibArc:

    def __init__(self, name: str, petriNet, origin, target, multiplicity=1):
        '''
        Create an instance of the Inhibitor Arc class.
        @param name: Name of the Inhibitor Arc, must be string, must be unique in assigned Petri Net
        @param petriNet: Reference of parent Petri Net element for Inhibitor Arc to be assigned to, must be instance of class PetriNet
        @param origin: Origin element of the Inhibitor Arc, must be instance Place
        @param target: Target element of the Inhibitor Arc, must be instance of class Timed Transition or Immediate Transition
        @param multiplicity: Multiplicity of the Inhibitor Arc, must be integer
        '''
        if(checkType(petriNet) == "PetriNet"):
            # reference of Petri Net consisting current Inhibitor Arc
            self.petriNet = petriNet

            if (checkName(petriNet, name)):
                # name of the Arc, recommended format: {Origin name}{Target name}InhibArc ie. WaitServiceInhibArc
                self.name = name

                # Adding reference of Inhibitor Arc to Origin's Inhibitor Arc list
                if(checkType(origin) == "Place"):
                    # reference of origin Place TODO: might change it to name and perform search in lists
                    self.origin = origin
                    origin.inhibArcs.append(self)
                else:
                    del self
                    raise Exception(
                        "Inhibitor Arc's origin parameter must be instance of class Place")

                # Adding reference of Inhibitor Arc to target Transition's Inhibitor Arc list
                if(checkType(target) == "TimedTransition"):
                    # reference of target Transition TODO: might change it to name and perform search in lists
                    self.target = target
                    target.inhibArcs.append(self)
                elif(checkType(target) == "ImmediateTransition"):
                    # reference of target Transition TODO: might change it to name and perform search in lists
                    self.target = target
                    target.inhibArcs.append(self)
                else:
                    del self
                    raise Exception(
                        "Inhibitor Arc's target parameter must be instance of class Timed Transition or Immediate Transition")

                # multiplicity of Arc
                if(checkType(multiplicity) == 'int'):
                    self.multiplicity = multiplicity
                elif(checkType(multiplicity()) == 'int'):
                    self.multiplicity = multiplicity
                else:
                    del self
                    raise Exception(
                        "The multiplicity of Inhibitor Arc named: " + name + " is invalid (must be integer or function call returning integer value)!")

                # add Inhibitor Arc to PN's Inhibitor Arc list
                petriNet.inhibList.append(self)

            else:
                del self
                raise Exception(
                    "An Inhibitor Arc already exists named: " + name + ", in Petri Net named: " + petriNet.name)

        else:
            del self
            raise Exception(
                "Petri Net with name: " + petriNet + " does not exist!")

    def __str__(self):
        '''
        Default return value of class, gives description of current state of Inhibitor.
        '''
        returnString = f'Inhibitor Arc (name: {self.name}, '
        returnString += f'in Petri Net named: {self.petriNet.name}, '
        if(self.origin is not None):
            returnString += f'from Place: {self.origin.name}, '
        else:
            returnString += f'from Place: {None}, '
        if(self.target is not None):
            if(checkType(self.target) == "TimedTransition"):
                returnString += f'to Timed Transition: {self.target.name}, '
            elif(checkType(self.target) == "ImmediateTransition"):
                returnString += f'to Immediate Transition: {self.target.name}, '
        else:
            returnString += f'to Transition: {None}, '
        returnString += f'multiplicity: {self.multiplicity}'

        return returnString

    # NAME
    def setName(self, newName: str):
        '''
        Setter function for name of Inhibitor.
        @param newName: New name for Inhibitor, must be string, must be unique in assigned Petri Net
        '''
        if (checkName(self.petriNet, newName)):
            self.name = newName
        else:
            raise Exception(
                "An Inhibitor Arc already exists named: " + newName + ", in Petri Net named: " + self.petriNet.name)

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
        @param newOrigin: New origin for Inhibitor, must be instance of class Place, must be assigned to same Petri Net instance
        '''
        if(checkType(newOrigin) == "Place"):
            if(newOrigin.petriNet != self.petriNet):
                raise Exception(
                    "Inhibitor Arc's new origin Place must be assigned to the same Petri Net of Inhibitor Arc!")
            if (self.origin is not None):
                if self in self.origin.inhibArcs:
                    # remove reference to Inhibitor Arc from old origin Place's Inhibitor Arc list
                    self.origin.inhibArcs.remove(self)
            # add reference to Inhibitor Arc to new origin Place's Inhibitor Arc list
            self.origin = newOrigin
            newOrigin.inhibArcs.append(self)
        else:
            raise Exception(
                "Inhibitor Arc's new origin parameter must be instance of class Place")

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
        @param newTarget: New target for Inhibitor, must be instance of class Timed Transition or Immediate Transition, must be assigned to same Petri Net instance
        '''
        if(checkType(newTarget) == "TimedTransition"):
            if(newTarget.petriNet != self.petriNet):
                raise Exception(
                    "Inhibitor Arc's new target Timed Transition must be assigned to the same Petri Net of Inhibitor Arc!")
            if (self.target is not None):
                if self in self.target.inhibArcs:
                    # remove reference to Inhibitor Arc from old target Transition's Inhibitor Arc list
                    self.target.inhibArcs.remove(self)
            # add reference to Inhibitor Arc to new target Transition's Inhibitor Arc list
            self.target = newTarget
            newTarget.inhibArcs.append(self)
        elif(checkType(newTarget) == "ImmediateTransition"):
            if(newTarget.petriNet != self.petriNet):
                raise Exception(
                    "Inhibitor Arc's new target Immediate Transition must be assigned to the same Petri Net of Inhibitor Arc!")
            if (self.target is not None):
                if self in self.target.inhibArcs:
                    self.target.inhibArcs.remove(self)
            # add reference to Inhibitor Arc to new target Transition's Inhibitor Arc list
            self.target = newTarget
            newTarget.inhibArcs.append(self)
        else:
            raise Exception(
                "Inhibitor Arc's new target parameter must be instance of class Timed Transition or Immediate Transition")

    def getTarget(self):
        '''
        Getter function for target of Inhibitor.
        Returns current target of Inhibitor.
        '''
        return self.target


def checkName(petriNet, name):
    for inhibArc in petriNet.inhibList:
        if (inhibArc.name == name):
            return False
    return True


def findInhibArcByName(name):
    for inhibArc in inhibList:
        if (inhibArc.name == name):
            return inhibArc
    raise Exception('Inhibitor Arc does not exists with name: ' + name)


def checkType(object):
    return object.__class__.__name__
