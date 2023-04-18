# components/inputArc.py module for Petri Net Project
# contains class definition for object type Input Arc

class InputArc:
    '''
    Class that represents an Input Arc object.
    '''

    def __init__(self, name: str, petriNet, fromPlace, toTrans, multiplicity=1):
        '''
        Constructor method of the Input Arc class.
        Arguments:
            @param name: Name of the Input Arc, must be string, must be unique amongst Input Arc names in assigned Petri Net.
            @param petriNet: Reference of parent Petri Net object for Input Arc to be assigned to, must be instance of class PetriNet.
            @param fromPlace: Origin object of the Input Arc, must be instance of class Place.
            @param toTrans: Target object of the Input Arc, must be instance of class Timed Transition or Immediate Transition.
            @param multiplicity: Multiplicity of the Input Arc, must be integer and greater than 0, or reference to a callable function defined in the user file, returning integer value, i.e. "Queue.tokens". Default value: 1.
        '''

        # Type checks
        if(_checkType(petriNet) == "PetriNet"):
            # set reference of Petri Net to assign current Input Arc to
            self.petriNet = petriNet

            if (_checkName(petriNet, name)):
                # set name of the Input Arc
                self.name = str(name)

                # add reference of Input Arc to origin Place's Input Arc list
                if(_checkType(fromPlace) == "Place"):
                    if(fromPlace.petriNet != petriNet):
                        del self
                        raise Exception(
                            "Input Arc's fromPlace parameter must be instance of class Place from the same assigned Petri Net")
                    # set reference of origin Place
                    self.fromPlace = fromPlace
                    fromPlace.inputArcs.append(self)
                else:
                    del self
                    raise Exception(
                        "Input Arc's fromPlace parameter must be instance of class Place")

                # add reference of Input Arc to target Transition's Input Arc list
                if(_checkType(toTrans) == "TimedTransition"):
                    if(toTrans.petriNet != petriNet):
                        del self
                        raise Exception(
                            "Input Arc's toTrans parameter must be instance of class Timed Transition or Immediate Transition from the same assigned Petri Net")
                    # set reference of target (Timed) Transition
                    self.toTrans = toTrans
                    toTrans.inputArcs.append(self)
                elif(_checkType(toTrans) == "ImmediateTransition"):
                    if(toTrans.petriNet != petriNet):
                        del self
                        raise Exception(
                            "Input Arc's toTrans parameter must be instance of class Timed Transition or Immediate Transition from the same assigned Petri Net")
                    # set reference of target (Immediate) Transition
                    self.toTrans = toTrans
                    toTrans.inputArcs.append(self)
                else:
                    del self
                    raise Exception(
                        "Input Arc's toTrans parameter must be instance of class Timed Transition or Immediate Transition")

                # set multiplicity of Input Arc
                if(_checkType(multiplicity) == 'int'):
                    # if multiplicity is a set integer, check if it's greater than 0
                    if(multiplicity <= 0):
                        del self
                        raise Exception(
                            "The multiplicity of Input Arc named: " + name + " must be greater than 0!"
                        )
                    else:
                        self.multiplicity = multiplicity
                # if multiplicity is set dynamically via function, check if it's returning integer value
                elif(_checkType(multiplicity()) == 'int'):
                    self.multiplicity = multiplicity
                else:
                    del self
                    raise Exception(
                        "The multiplicity of Input Arc named: " + name + " is invalid (must be integer or function call returning integer value)!")

                # add Input Arc to PN's Input Arc list
                petriNet.inputArcList.append(self)

            else:
                del self
                raise Exception(
                    "An Input Arc already exists named: " + name + ", in Petri Net named: " + petriNet.name)

        else:
            del self
            raise Exception(
                "Petri Net with name: " + petriNet + " does not exist!")

    def __str__(self):
        '''
        Returns user-friendly string representation (description) of Input Arc object.
        '''
        returnString = (
            f"Input Arc\n"
            f"\tname: {self.name},\n"
            f"\tin Petri Net named: {self.petriNet.name},\n"
        )
        if(self.fromPlace is not None):
            returnString += f"\tfrom Place: {self.fromPlace.name},\n"
        else:
            returnString += f"\tfrom Place: {None},\n"
        if(self.toTrans is not None):
            if(_checkType(self.toTrans) == "TimedTransition"):
                returnString += f"\tto Timed Transition: {self.toTrans.name},\n"
            elif(_checkType(self.toTrans) == "ImmediateTransition"):
                returnString += f"\tto Immediate Transition: {self.toTrans.name},\n"
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
        Setter function for name of Input Arc.
        @param newName: New name for Input Arc, must be string, must be unique in assigned Petri Net
        '''
        if (_checkName(self.petriNet, newName)):
            self.name = newName
        else:
            raise Exception(
                "An Input Arc already exists named: " + newName + ", in Petri Net named: " + self.petriNet.name)

    def getName(self):
        '''
        Getter function for name of Input Arc.
        Returns current name of Input Arc.
        '''
        return self.name

    # FROM PLACE
    def setFromPlace(self, fromPlace):
        '''
        Setter function for origin place of Input Arc.
        @param fromPlace: New origin place for Input Arc, must be instance of class Place, must be assigned to same Petri Net instance
        '''
        if(_checkType(fromPlace) == "Place"):
            if(fromPlace.petriNet != self.petriNet):
                raise Exception(
                    "Input Arc's new origin place parameter must be instance of class Place from the same assigned Petri Net")
            if (self.fromPlace is not None):
                if self in self.fromPlace.inputArcs:
                    # remove reference to input Arc from old origin Place's Input Arc list
                    self.fromPlace.inputArcs.remove(self)
            # add reference to input Arc to new origin Place's Input Arc list
            self.fromPlace = fromPlace
            fromPlace.inputArcs.append(self)
        else:
            raise Exception(
                "Input Arc's new origin place parameter must be instance of class Place")

    def getFromPlace(self):
        '''
        Getter function for origin place of Input Arc.
        Returns current origin place of Input Arc.
        '''
        return self.fromPlace

    # TO TRANS
    def setToTrans(self, toTrans):
        '''
        Setter function for target transition of Input Arc.
        @param toTrans: New target transition for Input Arc, must be instance of class Timed Transition of Immediate Transition, must be assigned to same Petri Net instance
        '''
        if(_checkType(toTrans) == "TimedTransition"):
            if(toTrans.petriNet != self.petriNet):
                raise Exception(
                    "Input Arc's new target transition parameter must be instance of class Timed Transition from the same assigned Petri Net")
            if (self.toTrans is not None):
                if self in self.toTrans.inputArcs:
                    # remove reference to input Arc from old target Timed Transition's Input Arc list
                    self.toTrans.inputArcs.remove(self)
            # add reference to input Arc to new target Timed Transition's Input Arc list
            self.toTrans = toTrans
            toTrans.inputArcs.append(self)
        elif(_checkType(toTrans) == "ImmediateTransition"):
            if(toTrans.petriNet != self.petriNet):
                raise Exception(
                    "Input Arc's new target transition parameter must be instance of class Immediate Transition from the same assigned Petri Net")
            if (self.toTrans is not None):
                if self in self.toTrans.inputArcs:
                    # remove reference to input Arc from old target Immediate Transition's Input Arc list
                    self.toTrans.inputArcs.remove(self)
            # add reference to input Arc to new target Immediate Transition's Input Arc list
            self.toTrans = toTrans
            toTrans.inputArcs.append(self)
        else:
            raise Exception(
                "Input Arc's new target transition parameter must be instance of class Timed Transition of Immediate Transition")

    def getToTrans(self):
        '''
        Getter function for target transition of Input Arc.
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


def _checkName(petriNet, name):
    for inputArc in petriNet.inputArcList:
        if (inputArc.name == name):
            return False
    return True


def _checkType(object):
    return object.__class__.__name__


# def findInputArcByName(name):
#     for inputArc in inputArcList:
#         if (inputArc.name == name):
#             return inputArc
#     raise Exception('Input Arc does not exists with name: ' + name)
