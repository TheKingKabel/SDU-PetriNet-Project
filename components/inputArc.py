
class InputArc:

    def __init__(self, name: str, petriNet, fromPlace, toTrans, multiplicity: int = 1):
        '''
        Create an instance of the Input Arc class.
        @param name: Name of the Input Arc, must be string, must be unique in assigned Petri Net
        @param petriNet: Reference of parent Petri Net element for Input Arc to be assigned to, must be instance of class PetriNet
        @param fromPlace: Origin place of the Input Arc, must be instance of class Place
        @param toTrans: Target transition of the Input Arc, must be instance of class Timed Transition or Immediate Transition
        @param multiplicity: Multiplicity of the Input Arc, must be integer
        '''
        if(checkType(petriNet) == "PetriNet"):
            # reference of Petri Net consisting current Input Arc
            self.petriNet = petriNet

            if (checkName(petriNet, name)):
                # name of the Arc, recommended format: {Origin name}{Target name}Arc ie. WaitServiceArc
                self.name = name

                # Adding reference of Input Arc to origin Place's Input Arc list
                if(checkType(fromPlace) == "Place"):
                    if(fromPlace.petriNet != petriNet):
                        del self
                        raise Exception(
                            "Input Arc's fromPlace parameter must be instance of class Place from the same assigned Petri Net")
                    # reference of origin Place TODO: might change it to name and perform search in placeList
                    self.fromPlace = fromPlace
                    fromPlace.inputArcs.append(self)
                else:
                    del self
                    raise Exception(
                        "Input Arc's fromPlace parameter must be instance of class Place")

                # Adding reference of Input Arc to target Transition's Input Arc list
                if(checkType(toTrans) == "TimedTransition"):
                    if(toTrans.petriNet != petriNet):
                        del self
                        raise Exception(
                            "Input Arc's toTrans parameter must be instance of class Timed Transition or Immediate Transition from the same assigned Petri Net")
                    # reference of target Timed Transition TODO: might change it to name and perform search in timedTransList
                    self.toTrans = toTrans
                    toTrans.inputArcs.append(self)
                elif(checkType(toTrans) == "ImmediateTransition"):
                    if(toTrans.petriNet != petriNet):
                        del self
                        raise Exception(
                            "Input Arc's toTrans parameter must be instance of class Timed Transition or Immediate Transition from the same assigned Petri Net")
                    # reference of target Immediate Transition TODO: might change it to name and perform search in immediateTransList
                    self.toTrans = toTrans
                    toTrans.inputArcs.append(self)
                else:
                    del self
                    raise Exception(
                        "Input Arc's toTrans parameter must be instance of class Timed Transition or Immediate Transition")

                # multiplicity of Arc
                self.multiplicity = multiplicity

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
        Default return value of class, gives description of current state of Input Arc.
        '''
        returnString = f'Input Arc (name: {self.name}, '
        returnString += f'in Petri Net named: {self.petriNet.name}, '
        if(self.fromPlace is not None):
            returnString += f'from Place: {self.fromPlace.name}, '
        else:
            returnString += f'from Place: {None}, '
        if(self.toTrans is not None):
            if(checkType(self.toTrans) == "TimedTransition"):
                returnString += f'to Timed Transition: {self.toTrans.name}, '
            elif(checkType(self.toTrans) == "ImmediateTransition"):
                returnString += f'to Immediate Transition: {self.toTrans.name}, '
        else:
            returnString += f'to Transition: {None}, '
        returnString += f'multiplicity: {self.multiplicity}'

        return returnString

    # NAME
    def setName(self, newName: str):
        '''
        Setter function for name of Input Arc.
        @param newName: New name for Input Arc, must be string, must be unique in assigned Petri Net
        '''
        if (checkName(self.petriNet, newName)):
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
        if(checkType(fromPlace) == "Place"):
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
        if(checkType(toTrans) == "TimedTransition"):
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
        elif(checkType(toTrans) == "ImmediateTransition"):
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


def checkName(petriNet, name):
    for inputArc in petriNet.inputArcList:
        if (inputArc.name == name):
            return False
    return True


def checkType(object):
    return object.__class__.__name__


# def findInputArcByName(name):
#     for inputArc in inputArcList:
#         if (inputArc.name == name):
#             return inputArc
#     raise Exception('Input Arc does not exists with name: ' + name)
