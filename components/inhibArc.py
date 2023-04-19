# components/inhibArc.py module for Petri Net Project
# contains class definition for object type Inhibitor Arc

class InhibArc:
    '''
    Class that represents an Inhibitor Arc object.
    '''

    def __init__(self, name: str, petriNet, origin, target, multiplicity=1):
        '''
        Constructor method of the Inhibitor Arc class.
        Arguments:
            @param name: Name of the Inhibitor Arc, must be string, must be unique amongst Inhibitor Arc names in assigned Petri Net.
            @param petriNet: Reference of parent Petri Net object for Inhibitor Arc to be assigned to, must be instance of class PetriNet.
            @param origin: Origin object of the Inhibitor Arc, must be instance of class Place.
            @param target: Target object of the Inhibitor Arc, must be instance of class Timed Transition or Immediate Transition.
            @param multiplicity: Multiplicity of the Inhibitor Arc, must be integer and greater than 0, or reference to a callable function defined in the user file, returning integer value, i.e. "Queue.tokens". Default value: 1.
        '''

        # Type checks
        if(_checkType(petriNet) == "PetriNet"):
            # set reference of Petri Net to assign current Inhibitor Arc to
            self.petriNet = petriNet

            if (_checkName(petriNet, name)):
                # set name of the Inhibitor Arc
                self.name = str(name)

                # add reference of Inhibitor Arc to Origin's Inhibitor Arc list
                if(_checkType(origin) == "Place"):
                    if(origin.petriNet != petriNet):
                        del self
                        raise Exception(
                            "Inhibitor Arc's origin parameter must be instance of class Place from the same assigned Petri Net")
                    # set reference of origin Place
                    self.origin = origin
                    origin.inhibArcs.append(self)
                else:
                    del self
                    raise Exception(
                        "Inhibitor Arc's origin parameter must be instance of class Place")

                # add reference of Inhibitor Arc to target Transition's Inhibitor Arc list
                if(_checkType(target) == "TimedTransition"):
                    if(target.petriNet != petriNet):
                        del self
                        raise Exception(
                            "Inhibitor Arc's target parameter must be instance of class Timed Transition or Immediate Transition from the same assigned Petri Net")
                    # set reference of target (Timed) Transition
                    self.target = target
                    target.inhibArcs.append(self)
                elif(_checkType(target) == "ImmediateTransition"):
                    if(target.petriNet != petriNet):
                        del self
                        raise Exception(
                            "Inhibitor Arc's target parameter must be instance of class Timed Transition or Immediate Transition from the same assigned Petri Net")
                    # set reference of target (Immediate) Transition
                    self.target = target
                    target.inhibArcs.append(self)
                else:
                    del self
                    raise Exception(
                        "Inhibitor Arc's target parameter must be instance of class Timed Transition or Immediate Transition")

                # set multiplicity of Inhibitor Arc
                if(_checkType(multiplicity) == 'int'):
                    # if multiplicity is a set integer, check if it's greater than 0
                    if(multiplicity <= 0):
                        del self
                        raise Exception(
                            "The multiplicity of Inhibitor Arc named: " + name + " must be greater than 0!"
                        )
                    else:
                        self.multiplicity = multiplicity
                # if multiplicity is set dynamically via function, check if it's returning integer value
                elif(_checkType(multiplicity()) == 'int'):
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
        Returns user-friendly string representation (description) of Inhibitor Arc object.
        '''
        returnString = (
            f"Inhibitor Arc\n"
            f"\tname: {self.name},\n"
            f"\tin Petri Net named: {self.petriNet.name},\n"
        )
        if(self.origin is not None):
            returnString += f"\tfrom Place: {self.origin.name},\n"
        else:
            returnString += f"\tfrom Place: {None},\n"
        if(self.target is not None):
            if(_checkType(self.target) == "TimedTransition"):
                returnString += f"\tto Timed Transition: {self.target.name},\n"
            elif(_checkType(self.target) == "ImmediateTransition"):
                returnString += f"\tto Immediate Transition: {self.target.name},\n"
        else:
            returnString += f"\tto Transition: {None},\n"
        returnString += f"\tmultiplicity: {self.multiplicity}\n"

        return returnString

    # TODO: delete getter setters, not needed?
    #
    #
    #

    # NAME
    def setName(self, newName: str):
        '''
        Setter function for name of Inhibitor.
        @param newName: New name for Inhibitor, must be string, must be unique in assigned Petri Net
        '''
        if (_checkName(self.petriNet, newName)):
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
        if(_checkType(newOrigin) == "Place"):
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
        if(_checkType(newTarget) == "TimedTransition"):
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
        elif(_checkType(newTarget) == "ImmediateTransition"):
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


def _checkName(petriNet, name):
    for inhibArc in petriNet.inhibList:
        if (inhibArc.name == name):
            return False
    return True


def findInhibArcByName(name):
    for inhibArc in inhibList:
        if (inhibArc.name == name):
            return inhibArc
    raise Exception('Inhibitor Arc does not exists with name: ' + name)


def _checkType(object):
    return object.__class__.__name__
