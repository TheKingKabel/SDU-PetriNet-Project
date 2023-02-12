from PetriNet import immediateTransList


class ImmediateTransition:

    def __init__(self, name: str, guard: str = None, fireProbability: float = 1.0, fireCount: int = 0):
        '''
        Create an instance of the Immediate Transition class.
        @param name: Unique name of the Immediate Transition, must be string
        @param guard: Condition for Immediate Transition to be enabled for firing, must be assessable logic statement in string, i.e. "Queue.tokens >= 1"
        @param fireProbability: Variable used to calculate firing probability, must be float
        @param fireCount: Variable used to count the number of firings of Immediate Transition for statistics, must be integer
        '''
        if (checkName(name)):
            # name of the Immediate Transition, must be unique
            self.name = name

            # set guard function if correctly specified, set to None if not applicable
            if(guard is not None):
                try:
                    eval(guard)
                except:
                    del self
                    raise Exception(
                        "The guard function added to Immediate Transition named: " + name + " is invalid")
                else:
                    # set guard function
                    self.guard = guard
            else:
                # guard is not specified
                self.guard = guard

            # probability of firing, default 1.0 (100%)
            self.fireProbability = fireProbability

            # number of times Immediate Transition has fired, default 0
            self.fireCount = fireCount

            # Immediate Transition enabled for firing, default: False, to be overwritten during simulation
            self.enabled = False

            # list of Input Arcs targeting current Immediate Transition
            self.inputArcs = []

            # list of Output Arcs originating from current Immediate Transition
            self.outputArcs = []

            # list of Inhibitor Arcs targeting the current Immediate Transition
            self.inhibArcs = []

            # add Immediate Transition to PN's Immediate Transition list
            immediateTransList.append(self)

        else:
            del self
            raise Exception(
                "An Immediate Transition already exists named: " + name)

    def __str__(self):
        '''
        Default return value of class, gives description of current state of Immediate Transition.
        '''
        returnString = (
            f"Immediate Transition (name={self.name}, "
            f"with guard function={self.guard}, "
            f"currently enabled={self.enabled}, "
            f"firing probability={self.fireProbability}, "
            f"times fired={self.fireCount}, "
            f"list of targeting Input Arcs={str(self.inputArcs)}, "
            f"list of originating Output Arcs={str(self.outputArcs)}, "
            f"list of targeting Inhibitor Arcs={str(self.inhibArcs)}, "
        )
        return returnString

    # NAME
    def setName(self, newName: str):
        '''
        Setter function for name of Immediate Transition.
        @param newName: Unique new name for Immediate Transition, must be string
        '''
        if (checkName(newName)):
            self.name = newName
        else:
            raise Exception(
                "An Immediate Transition already exists named: " + newName)

    def getName(self):
        '''
        Getter function for name of Immediate Transition.
        Returns current name of Immediate Transition.
        '''
        return self.name

    # GUARD
    def setGuard(self, guard: str):
        '''
        Setter function for guard condition of Immediate Transition.
        @param guard: New guard condition for Immediate Transition to enable firing, must be assessable logic statement in string, i.e. "Queue.tokens >= 1"
        '''
        if(guard is not None):
            try:
                eval(guard)
            except:
                raise Exception(
                    "The guard condition set for Immediate Transition must be valid")
            else:
                self.guard = guard
        else:
            self.guard = guard

    def getGuard(self):
        '''
        Getter function for guard condition of Immediate Transition.
        Returns current guard condition of Immediate Transition.
        '''
        return self.guard

    # FIRE PROBABILITY
    def setFireProbability(self, fireProbability: float):
        '''
        Setter function for firing probability of Immediate Transition.
        @param fireProbability: New firing probability for Immediate Transition, must be float
        '''
        self.fireProbability = fireProbability

    def getFireProbability(self):
        '''
        Getter function for firing probability of Immediate Transition.
        Returns current firing probability of Immediate Transition.
        '''
        return self.fireProbability

    # FIRE COUNT
    def setFireCount(self, fireCount: int):
        '''
        Setter function for fire count of Immediate Transition.
        @param fireCount: New fire count for Immediate Transition, must be integer
        '''
        self.fireCount = fireCount

    def getFireCount(self):
        '''
        Getter function for fire count of Immediate Transition.
        Returns current fire count of Immediate Transition.
        '''
        return self.fireCount

    # INPUT ARCS
    def setInputArcs(self, *inputArcList):
        '''
        Setter function to overwrite multiple Input Arcs targeting current Immediate Transition.
        Note: this function deletes existing list of Input Arcs, and creates new list with the given Input Arcs. To add single new Input Arc to Immediate Transition's Input Arc list, use addInputArc.
        @param *inputArcList: New tuple of Input Arcs to be added to Immediate Transition's Input Arc list, must be a tuple of instances of class Input Arc
        '''
        for arc in inputArcList:
            if(checkType(arc) != "InputArc"):
                raise Exception(
                    "Immediate Transition's new Input Arc list's elements must be instances of class Input Arc")
        self.inputArcs.clear
        for arc in inputArcList:
            arc.setToTrans(self)
            self.inputArcs.append(arc)

    def getInputArcs(self):
        '''
        Getter function for list of Input Arcs targeting current Immediate Transition.
        Returns current list of Input Arcs targeting current Immediate Transition.
        '''
        return self.inputArcs

    def addInputArc(self, newInputArc):
        '''
        Setter function to add new Input Arc targeting current Immediate Transition, to Immediate Transition's Input Arc list.
        Note: this function adds one new Input Arc to the Immediate Transition's Input Arc list. To overwrite the list with a tuple of multiple Input Arcs, use setInputArcs.
        @param newInputArc: New Input Arc to be added to Immediate Transition's Input Arc list, must be instance of class Input Arc
        '''
        if(checkType(newInputArc) != "InputArc"):
            raise Exception(
                "Immediate Transition's new Input Arc must be instance of class Input Arc")
        newInputArc.setToTrans(self)
        self.inputArcs.append(newInputArc)

    # OUTPUT ARCS
    def setOutputArcs(self, *outputArcList):
        '''
        Setter function to overwrite Output Arcs originating from current Immediate Transition.
        Note: this function deletes existing list of Output Arcs, and creates new list with the given parameters. To add single new Output Arc to Immediate Transition's Output Arc list, use addOutputArc.
        @param *outputArcList: New tuple of Output Arcs to be added to Immediate Transition's Output Arc list, must be a tuple of instances of class Output Arc
        '''
        for arc in outputArcList:
            if(checkType(arc) != "OutputArc"):
                raise Exception(
                    "Immediate Transition's new Output Arc list's elements must be instances of class Output Arc")
        self.outputArcs.clear
        for arc in outputArcList:
            arc.setFromTrans(self)
            self.outputArcs.append(arc)

    def getOutputArcs(self):
        '''
        Getter function for list of Output Arcs originating from current Immediate Transition.
        Returns current list of Output Arcs originating from current Immediate Transition.
        '''
        return self.outputArcs

    def addOutputArc(self, newOutputArc):
        '''
        Setter function to add new Output Arc originating from current Immediate Transition, to Immediate Transition's Output Arc list.
        Note: this function adds one new Output Arc to the Immediate Transition's Output Arc list. To overwrite the list with a tuple of multiple Output Arcs, use setOutputArcs.
        @param newOutputArc: New Output Arc to be added to Immediate Transition's Output Arc list, must be instance of class Output Arc
        '''
        if(checkType(newOutputArc) != "OutputArc"):
            raise Exception(
                "Immediate Transition's new Output Arc must be instance of class Output Arc")
        newOutputArc.setFromTrans(self)
        self.outputArcs.append(newOutputArc)

    # INHIB ARCS
    def setInhibArcs(self, *inhibArcList):
        '''
        Setter function to overwrite Inhibitor Arcs targeting current Immediate Transition.
        Note: this function deletes existing list of Inhibitor Arcs, and creates new list with the given parameters. To add single new Inhibitor Arc to Immediate Transition's Inhibitor Arc list, use addInhibArc.
        @param *inhibArcList: New tuple of Inhibitor Arcs to be added to Immediate Transition's Inhibitor Arc list, must be a tuple of instances of class Inhibitor Arc
        '''
        for arc in inhibArcList:
            if(checkType(arc) != "InhibArc"):
                raise Exception(
                    "Immediate Transition's new Inhibitor Arc list's elements must be instances of class Inhibitor Arc")
        self.inhibArcs.clear
        for arc in inhibArcList:
            arc.setTarget(self)
            self.inhibArcs.append(arc)

    def getInhibArcs(self):
        '''
        Getter function for list of Inhibitor Arcs targeting current Immediate Transition.
        Returns current list of Inhibitor Arcs targeting current Immediate Transition.
        '''
        return self.inhibArcs

    def addInhibArc(self, newInhibArc):
        '''
        Setter function to add new Inhibitor Arc targeting current Immediate Transition, to Immediate Transition's Inhibitor Arc list.
        Note: this function adds one new Inhibitor Arc to the Immediate Transition's Inhibitor Arc list. To overwrite the list with a tuple of multiple Inhibitor Arcs, use setInhibArcs.
        @param newInhibArc: New Inhibitor Arc to be added to Immediate Transition's Inhibitor Arc list, must be instance of class Inhibitor Arc
        '''
        if(checkType(newInhibArc) != "InhibArc"):
            raise Exception(
                "Immediate Transition's new Inhibitor Arc must be instance of class Inhibitor Arc")
        newInhibArc.setTarget(self)
        self.inhibArcs.append(newInhibArc)


def checkName(name):
    for trans in immediateTransList:
        if (trans.name == name):
            return False
    return True


def findTransitionByName(name):
    for trans in immediateTransList:
        if (trans.name == name):
            return trans
    raise Exception(
        'An Immediate Transition does not exists with name: ' + name)


def checkType(object):
    return object.__class__.__name__
