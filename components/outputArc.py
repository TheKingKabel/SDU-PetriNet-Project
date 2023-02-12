from main import outputEdgeList


class OutputArc:

    def __init__(self, name: str, fromTrans, toPlace, multiplicity: int = 1):
        '''
        Create an instance of the Output Arc class.
        @param name: Unique name of the Output Arc, must be string
        @param fromTrans: Origin transition of the Output Arc, must be instance of class Timed Transition or Instant Transition
        @param toPlace: Target place of the Output Arc, must be instance of class Place
        @param multiplicity: Multiplicity of the Output Arc, must be integer
        '''
        if (checkName(name)):
            # name of the arc, recommended format: {Origin trans name}{Target place name}Arc ie. WaitServiceArc
            self.name = name

            # Adding reference of Output Arc to Origin Transition's Output Arc list
            if(checkType(fromTrans) == "TimedTransition"):
                # reference of origin Transition TODO: might change it to name and perform search in transList
                self.fromTrans = fromTrans
                fromTrans.addOutputArcs(self)
            elif(checkType(fromTrans) == "InstantTransition"):
                # reference of origin Transition TODO: might change it to name and perform search in transList
                self.fromTrans = fromTrans
                fromTrans.addOutputArcs(self)
            else:
                del self
                raise Exception(
                    "Output Arc's fromTrans parameter must be instance of class Timed Transition or Instant Transition")

            # Adding reference of Output Arc to Target Place's Output Arc list
            if(checkType(toPlace) == "Place"):
                # reference of target Place TODO: might change it to name and perform search in placeList
                self.toPlace = toPlace
                toPlace.addOutputArcs(self)
            else:
                del self
                raise Exception(
                    "Output Arc's toPlace parameter must be instance of class Place")

            # multiplicity of arc
            self.multiplicity = multiplicity

            outputEdgeList.append(self)

        else:
            del self
            raise Exception("Output Arc already exists named: " + name)

    def __str__(self):
        '''
        Default return value of class, gives description of current state of Output Arc.
        '''
        returnString = f'Output Arc (name={self.name}, '
        if(checkType(self.fromTrans) == "TimedTransition"):
            returnString += f'from Timed Transition={self.fromTrans.name}, '
        elif(checkType(self.fromTrans) == "InstantTransition"):
            returnString += f'from Immediate Transition={self.fromTrans.name}, '
        returnString += f'to Place={self.toPlace.name}, '
        returnString += f'multiplicity={self.multiplicity}'

        return returnString

    # NAME
    def setName(self, newName: str):
        '''
        Setter function for name of Output Arc.
        @param newName: Unique new name for Output Arc, must be string
        '''
        if (checkName(newName)):
            self.name = newName
        else:
            raise Exception("An Output Arc already exists named: " + newName)

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
        @param fromTrans: New origin place for Output Arc, must be instance of class Timed Transition or Instant Transition
        '''
        if(checkType(fromTrans) == "TimedTransition"):
            if self in self.fromTrans.outputArcs:
                # remove reference to output Arc from old origin timed transition's outbound Output Arc list
                self.fromTrans.outputArcs.remove(self)
            # add reference to output Arc to new origin timed transition's outbound Output Arc list
            fromTrans.addOutputArcs(self)
        elif(checkType(fromTrans) == "InstantTransition"):
            if self in self.fromTrans.outputArcs:
                # remove reference to output Arc from old origin instant transition's outbound Output Arc list
                self.fromTrans.outputArcs.remove(self)
            # add reference to output Arc to new origin instant transition's outbound Output Arc list
            fromTrans.addOutputArcs(self)
        else:
            raise Exception(
                "Output Arc's new origin transition parameter must be instance of class Timed Transition of Instant Transition")
        self.fromTrans = fromTrans

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
        @param toPlace: New target place for Output Arc, must be instance of class Place
        '''
        if(checkType(toPlace) == "Place"):
            if self in self.toPlace.outputArcs:
                # remove reference to output Arc from old target place's inbound Output Arc list
                self.toPlace.outputArcs.remove(self)
            # add reference to output Arc to new target place's inbound Output Arc list
            toPlace.addOutputArcs(self)
        else:
            raise Exception(
                "Output Arc's new target place parameter must be instance of class Place")
        self.toPlace = toPlace

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


def checkName(name):
    for outputEdge in outputEdgeList:
        if (outputEdge.name == name):
            return False
    return True


def findOutputEdgeByName(name):
    for outputEdge in outputEdgeList:
        if (outputEdge.name == name):
            return outputEdge
    raise Exception('Output Arc does not exists with name: ' + name)


def checkType(object):
    return object.__class__.__name__
