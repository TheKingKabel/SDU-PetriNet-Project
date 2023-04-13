
class OutputArc:

    def __init__(self, name: str, petriNet, fromTrans, toPlace, multiplicity: int = 1):
        '''
        Create an instance of the Output Arc class.
        @param name: Name of the Output Arc, must be string, must be unique in assigned Petri Net
        @param petriNet: Reference of parent Petri Net element for Output Arc to be assigned to, must be instance of class PetriNet
        @param fromTrans: Origin transition of the Output Arc, must be instance of class Timed Transition or Immediate Transition
        @param toPlace: Target place of the Output Arc, must be instance of class Place
        @param multiplicity: Multiplicity of the Output Arc, must be integer
        '''
        if(checkType(petriNet) == "PetriNet"):
            # reference of Petri Net consisting current Output Arc
            self.petriNet = petriNet

            if (checkName(petriNet, name)):
                # name of the Arc, recommended format: {Origin name}{Target name}Arc ie. WaitServiceArc
                self.name = name

                # Adding reference of Output Arc to Origin Transition's Output Arc list
                if(checkType(fromTrans) == "TimedTransition"):
                    if(fromTrans.petriNet != petriNet):
                        del self
                        raise Exception(
                            "Output Arc's fromTrans parameter must be instance of class Timed Transition or Immediate Transition from the same assigned Petri Net")
                    # reference of origin Transition TODO: might change it to name and perform search in transList
                    self.fromTrans = fromTrans
                    fromTrans.outputArcs.append(self)
                elif(checkType(fromTrans) == "ImmediateTransition"):
                    if(fromTrans.petriNet != petriNet):
                        del self
                        raise Exception(
                            "Output Arc's fromTrans parameter must be instance of class Timed Transition or Immediate Transition from the same assigned Petri Net")
                    # reference of origin Transition TODO: might change it to name and perform search in transList
                    self.fromTrans = fromTrans
                    fromTrans.outputArcs.append(self)
                else:
                    del self
                    raise Exception(
                        "Output Arc's fromTrans parameter must be instance of class Timed Transition or Immediate Transition")

                # Adding reference of Output Arc to Target Place's Output Arc list
                if(checkType(toPlace) == "Place"):
                    if(toPlace.petriNet != petriNet):
                        del self
                        raise Exception(
                            "Output Arc's toPlace parameter must be instance of class Place from the same assigned Petri Net")
                    # reference of target Place TODO: might change it to name and perform search in placeList
                    self.toPlace = toPlace
                    toPlace.outputArcs.append(self)
                else:
                    del self
                    raise Exception(
                        "Output Arc's toPlace parameter must be instance of class Place")

                # multiplicity of Arc
                if(checkType(multiplicity) == 'int'):
                    if(multiplicity <= 0):
                        del self
                        raise Exception(
                            "The multiplicity of Inhibitor Arc named: " + name + " must be greater than 0!"
                        )
                    else:
                        self.multiplicity = multiplicity
                elif(checkType(multiplicity()) == 'int'):
                    self.multiplicity = multiplicity
                else:
                    del self
                    raise Exception(
                        "The multiplicity of Input Arc named: " + name + " is invalid (must be integer or function call returning integer value)!")

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
        Default return value of class, gives description of current state of Output Arc.
        '''
        returnString = f'Output Arc (name: {self.name}, '
        returnString += f'in Petri Net named: {self.petriNet.name}, '
        if(self.fromTrans is not None):
            if(checkType(self.fromTrans) == "TimedTransition"):
                returnString += f'from Timed Transition: {self.fromTrans.name}, '
            elif(checkType(self.fromTrans) == "ImmediateTransition"):
                returnString += f'from Immediate Transition: {self.fromTrans.name}, '
        else:
            returnString += f'from Transition: {None}, '
        if(self.toPlace is not None):
            returnString += f'to Place: {self.toPlace.name}, '
        else:
            returnString += f'to Place: {None}, '
        returnString += f'multiplicity: {self.multiplicity}'

        return returnString

    # NAME
    def setName(self, newName: str):
        '''
        Setter function for name of Output Arc.
        @param newName: New name for Output Arc, must be string, must be unique in assigned Petri Net
        '''
        if (checkName(self.petriNet, newName)):
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
        if(checkType(fromTrans) == "TimedTransition"):
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
        elif(checkType(fromTrans) == "ImmediateTransition"):
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
        if(checkType(toPlace) == "Place"):
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


def checkName(petriNet, name):
    for outputArc in petriNet.outputArcList:
        if (outputArc.name == name):
            return False
    return True


def findOutputArcByName(name):
    for outputArc in outputArcList:
        if (outputArc.name == name):
            return outputArc
    raise Exception('Output Arc does not exists with name: ' + name)


def checkType(object):
    return object.__class__.__name__
