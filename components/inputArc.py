from main import inputEdgeList


class InputArc:

    def __init__(self, name: str, fromPlace, toTrans, multiplicity: int = 1):
        '''
        Create an instance of the Input Arc class.
        @param name: Unique name of the Input Arc, must be string
        @param fromPlace: Origin place of the Input Arc, must be instance of class Place
        @param toTrans: Target transition of the Input Arc, must be instance of class Timed Transition or Immediate Transition
        @param multiplicity: Multiplicity of the Input Arc, must be integer
        '''
        if (checkName(name)):
            # name of the Arc, recommended format: {Origin name}{Target name}Arc ie. WaitServiceArc
            self.name = name

            # Adding reference of Input Arc to origin Place's Input Arc list
            if(checkType(fromPlace) == "Place"):
                # reference of origin Place TODO: might change it to name and perform search in placeList
                self.fromPlace = fromPlace
                fromPlace.addInputArcs(self)
            else:
                del self
                raise Exception(
                    "Input Arc's fromPlace parameter must be instance of class Place")

            # Adding reference of Input Arc to target Transition's Input Arc list
            if(checkType(toTrans) == "TimedTransition"):
                self.toTrans = toTrans
                toTrans.addInputArcs(self)
            elif(checkType(toTrans) == "ImmediateTransition"):
                self.toTrans = toTrans
                toTrans.addInputArcs(self)
            else:
                del self
                raise Exception(
                    "Input Arc's toTrans parameter must be instance of class Timed Transition or Immediate Transition")

            # multiplicity of Arc
            self.multiplicity = multiplicity

            # append to list of current PN net of input Arcs
            inputEdgeList.append(self)

        else:
            del self
            raise Exception("Input Arc already exists named: " + name)

    def __str__(self):
        '''
        Default return value of class, gives description of current state of Input Arc.
        '''
        returnString = f'Input Arc (name={self.name}, '
        returnString += f'from Place={self.fromPlace.name}, '
        if(checkType(self.toTrans) == "TimedTransition"):
            returnString += f'to Timed Transition={self.toTrans.name}, '
        elif(checkType(self.toTrans) == "ImmediateTransition"):
            returnString += f'to Immediate Transition={self.toTrans.name}, '
        returnString += f'multiplicity={self.multiplicity}'

        return returnString

    # NAME
    def setName(self, newName: str):
        '''
        Setter function for name of Input Arc.
        @param newName: Unique new name for Input Arc, must be string
        '''
        if (checkName(newName)):
            self.name = newName
        else:
            raise Exception("An Input Arc already exists named: " + newName)

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
        @param fromPlace: New origin place for Input Arc, must be instance of class Place
        '''
        if(checkType(fromPlace) == "Place"):
            if self in self.fromPlace.inputArcs:
                # remove reference to input Arc from old origin Place's Input Arc list
                self.fromPlace.inputArcs.remove(self)
            # add reference to input Arc to new origin Place's Input Arc list
            fromPlace.addInputArcs(self)
        else:
            raise Exception(
                "Input Arc's new origin place parameter must be instance of class Place")
        self.fromPlace = fromPlace

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
        @param toTrans: New target transition for Input Arc, must be instance of class Timed Transition of Immediate Transition
        '''
        if(checkType(toTrans) == "TimedTransition"):
            if self in self.toTrans.inputArcs:
                # remove reference to input Arc from old target Timed Transition's Input Arc list
                self.toTrans.inputArcs.remove(self)
            # add reference to input Arc to new target Timed Transition's Input Arc list
            toTrans.addInputArcs(self)
        elif(checkType(toTrans) == "ImmediateTransition"):
            if self in self.toTrans.inputArcs:
                # remove reference to input Arc from old target Immediate Transition's Input Arc list
                self.toTrans.inputArcs.remove(self)
            # add reference to input Arc to new target Immediate Transition's Input Arc list
            toTrans.addInputArcs(self)
        else:
            raise Exception(
                "Input Arc's new target transition parameter must be instance of class Timed Transition of Immediate Transition")
        self.toTrans = toTrans

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


def checkName(name):
    for inputEdge in inputEdgeList:
        if (inputEdge.name == name):
            return False
    return True


def findInputEdgeByName(name):
    for inputEdge in inputEdgeList:
        if (inputEdge.name == name):
            return inputEdge
    raise Exception('Input Arc does not exists with name: ' + name)


def checkType(object):
    return object.__class__.__name__
