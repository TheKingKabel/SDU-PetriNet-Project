# outputArc.py module for Petri Net Project
# contains class definition for object type output Arc

class OutputArc:
    '''
    Class that represents an Output Arc object.
    '''

    def __init__(self, name: str, petriNet, fromTrans, toPlace, multiplicity=1):
        '''
        Constructor method of the Output Arc class.
        Arguments:
            @param name: Name of the Output Arc, must be string, must be unique amongst Output Arc names in assigned Petri Net.
            @param petriNet: Reference of parent Petri Net object for Output Arc to be assigned to, must be instance of class PetriNet.
            @param fromTrans: Origin object of the Output Arc, must be instance of class Timed Transition or Immediate Transition.
            @param toPlace: Target object of the Output Arc, must be instance of class Place.
            @param multiplicity: Multiplicity of the Output Arc, must be integer and greater than 0, or reference to a callable function defined in the user file, returning integer value, i.e. "Queue.tokens". Default value: 1.
        '''

        # Type checks
        if(_checkType(petriNet) == "PetriNet"):
            # set reference of Petri Net to assign current Output Arc to
            self.petriNet = petriNet

            if (_checkName(petriNet, name)):
                # set name of the Output Arc
                self.name = name

                # add reference of Output Arc to origin Transition's Output Arc list
                if(_checkType(fromTrans) == "TimedTransition"):
                    if(fromTrans.petriNet != petriNet):
                        del self
                        raise Exception(
                            "Output Arc's fromTrans parameter must be instance of class Timed Transition or Immediate Transition from the same assigned Petri Net")
                    # set reference of origin (Timed) Transition
                    self.fromTrans = fromTrans
                    fromTrans.outputArcs.append(self)
                elif(_checkType(fromTrans) == "ImmediateTransition"):
                    if(fromTrans.petriNet != petriNet):
                        del self
                        raise Exception(
                            "Output Arc's fromTrans parameter must be instance of class Timed Transition or Immediate Transition from the same assigned Petri Net")
                    # set reference of origin (immediate) Transition
                    self.fromTrans = fromTrans
                    fromTrans.outputArcs.append(self)
                else:
                    del self
                    raise Exception(
                        "Output Arc's fromTrans parameter must be instance of class Timed Transition or Immediate Transition")

                # add reference of Output Arc to target Place's Output Arc list
                if(_checkType(toPlace) == "Place"):
                    if(toPlace.petriNet != petriNet):
                        del self
                        raise Exception(
                            "Output Arc's toPlace parameter must be instance of class Place from the same assigned Petri Net")
                    # set reference of target Place
                    self.toPlace = toPlace
                    toPlace.outputArcs.append(self)
                else:
                    del self
                    raise Exception(
                        "Output Arc's toPlace parameter must be instance of class Place")

                # set multiplicity of Output Arc
                if(_checkType(multiplicity) == 'int'):
                    # if multiplicity is a set integer, check if it's greater than 0
                    if(multiplicity <= 0):
                        del self
                        raise Exception(
                            "The multiplicity of Output Arc named: " + name + " must be greater than 0!"
                        )
                    else:
                        self.multiplicity = multiplicity
                # if multiplicity is set dynamically via function, check if it's returning integer value
                elif(_checkType(multiplicity()) == 'int'):
                    self.multiplicity = multiplicity
                else:
                    del self
                    raise Exception(
                        "The multiplicity of Output Arc named: " + name + " is invalid (must be integer or function call returning integer value)!")

                # add Output Arc to PN's Output Arc list
                petriNet.outputArcList.append(self)

            else:
                del self
                raise Exception(
                    "An Output Arc already exists named: " + name + ", in Petri Net named: " + petriNet.name)

        else:
            del self
            raise Exception(
                "Petri Net with name: " + petriNet + " does not exist!")

    def __str__(self):
        '''
        Returns user-friendly string representation (description) of Output Arc object.
        '''
        returnString = (
            f"Output Arc\n"
            f"\tname: {self.name},\n"
            f"\tin Petri Net named: {self.petriNet.name},\n"
        )
        if(self.fromTrans is not None):
            if(_checkType(self.fromTrans) == "TimedTransition"):
                returnString += f"\tfrom Timed Transition: {self.fromTrans.name},\n"
            elif(_checkType(self.fromTrans) == "ImmediateTransition"):
                returnString += f"\tfrom Immediate Transition: {self.fromTrans.name},\n"
        else:
            returnString += f"\tfrom Transition: {None},\n"
        if(self.toPlace is not None):
            returnString += f"\tto Place: {self.toPlace.name},\n"
        else:
            returnString += f"\tto Place: {None},\n"
        returnString += f"\tmultiplicity: {self.multiplicity}\n"

        return returnString

    # TODO: delete getter setters, not needed?
    #
    #
    #

    # NAME
    def setName(self, newName: str):
        '''
        Setter function for name of Output Arc.
        @param newName: New name for Output Arc, must be string, must be unique in assigned Petri Net
        '''
        if (_checkName(self.petriNet, newName)):
            self.name = newName
        else:
            raise Exception(
                "An Output Arc already exists named: " + newName + ", in Petri Net named: " + self.petriNet.name)

    def getName(self):
        '''
        Getter function for name of Output Arc.
        Returns current name of Output Arc.
        '''
        return self.name

    # FROM TRANS
    def setFromTrans(self, fromTrans):
        '''
        Setter function for origin transition of Output Arc.
        @param fromTrans: New origin place for Output Arc, must be instance of class Timed Transition or Immediate Transition, must be assigned to same Petri Net instance
        '''
        if(_checkType(fromTrans) == "TimedTransition"):
            if(fromTrans.petriNet != self.petriNet):
                raise Exception(
                    "Output Arc's new origin transition parameter must be instance of class Timed Transition from the same assigned Petri Net")
            if (self.fromTrans is not None):
                if self in self.fromTrans.outputArcs:
                    # remove reference to output Arc from old origin Timed Transition's Output Arc list
                    self.fromTrans.outputArcs.remove(self)
            # add reference to output Arc to new origin Timed Transition's Output Arc list
            self.fromTrans = fromTrans
            fromTrans.outputArcs.append(self)
        elif(_checkType(fromTrans) == "ImmediateTransition"):
            if(fromTrans.petriNet != self.petriNet):
                raise Exception(
                    "Output Arc's new origin transition parameter must be instance of class Immediate Transition from the same assigned Petri Net")
            if (self.fromTrans is not None):
                if self in self.fromTrans.outputArcs:
                    # remove reference to output Arc from old origin Immediate Transition's Output Arc list
                    self.fromTrans.outputArcs.remove(self)
            # add reference to output Arc to new origin Immediate Transition's Output Arc list
            self.fromTrans = fromTrans
            fromTrans.outputArcs.append(self)
        else:
            raise Exception(
                "Output Arc's new origin transition parameter must be instance of class Timed Transition of Immediate Transition")

    def getFromTrans(self):
        '''
        Getter function for origin transition of Output Arc.
        Returns current origin transition of Output Arc.
        '''
        return self.fromTrans

    # TO PLACE
    def setToPlace(self, toPlace):
        '''
        Setter function for target place of Output Arc.
        @param toPlace: New target place for Output Arc, must be instance of class Place, must be assigned to same Petri Net instance
        '''
        if(_checkType(toPlace) == "Place"):
            if(toPlace.petriNet != self.petriNet):
                raise Exception(
                    "Output Arc's new target place parameter must be instance of class Place from the same assigned Petri Net")
            if (self.toPlace is not None):
                if self in self.toPlace.outputArcs:
                    # remove reference to output Arc from old target Place's Output Arc list
                    self.toPlace.outputArcs.remove(self)
            # add reference to output Arc to new target Place's Output Arc list
            self.toPlace = toPlace
            toPlace.outputArcs.append(self)
        else:
            raise Exception(
                "Output Arc's new target place parameter must be instance of class Place")

    def getToPlace(self):
        '''
        Getter function for target place of Output Arc.
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


def _checkName(petriNet, name):
    for outputArc in petriNet.outputArcList:
        if (outputArc.name == name):
            return False
    return True


def findOutputArcByName(name):
    for outputArc in outputArcList:
        if (outputArc.name == name):
            return outputArc
    raise Exception('Output Arc does not exists with name: ' + name)


def _checkType(object):
    return object.__class__.__name__
