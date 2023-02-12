from PetriNet import timedTransList


class TimedTransition:

    def __init__(self, name: str, distType, agePolicy, guard: str = None, fireCount: int = 0):
        '''
        Create an instance of the Timed Transition class.
        @param name: Unique name of the Timed Transition, must be string
        @param distType: Distribution type of random firings of the Timed Transition, must be chosen from predetermined enumeration         TODO: implement enumeration, define default
        @param agePolicy: Setting to able/disable race age of Timed Transition, must be chosen from predetermined enumeration               TODO: implement enumeration, define default
        @param guard: Condition for Timed Transition to be enabled for firing, must be assessable logic statement in string, i.e. "Queue.tokens >= 1"
        @param fireCount: Variable used to count the number of firings of Timed Transition for statistics, must be integer
        '''
        if (checkName(name)):
            # name of the Immediate Transition, must be unique
            self.name = name

            # type of distribution                  TODO: implement
            self.distType = distType

            # age policy setting of transition      TODO: implement race enabled/disabled
            self.agePolicy = agePolicy

            # set guard function if correctly specified, set to None if not applicable
            if(guard is not None):
                try:
                    eval(guard)
                except:
                    del self
                    raise Exception(
                        "The guard function added to Timed Transition named: " + name + " is invalid")
                else:
                    # set guard function
                    self.guard = guard
            else:
                # guard is not specified
                self.guard = guard

            # number of times Timed Transition has fired, default 0
            self.fireCount = fireCount

            # Timed Transition enabled for firing, default: False, to be overwritten during simulation
            self.enabled = False

            # list of Input Arcs targeting the current Timed Transition
            self.inputArcs = []

            # list of Output Arcs originating from current Timed Transition
            self.outputArcs = []

            # list of inbound Inhibitor Arcs targeting the current Timed Transition
            self.inhibArcs = []

            # add Timed Transition to PN's Timed Transition list
            timedTransList.append(self)

        else:
            del self
            raise Exception("A Timed Transition already exists named: " + name)

    def __str__(self):
        '''
        Default return value of class, gives description of current state of Timed Transition.
        '''
        returnString = (
            f"Timed Transition (name={self.name}, "
            f"with distribution type={self.distType}, "
            f"with guard function={self.guard}, "
            f"currently enabled={self.enabled}, "
            f"age policy={self.agePolicy}, "
            f"times fired={self.fireCount}, "
            f"list of targeting Input Arcs={str(self.inputArcs)}, "
            f"list of originating Output Arcs={str(self.outputArcs)}, "
            f"list of targeting Inhibitor Arcs={str(self.inhibArcs)}, "
        )
        return returnString

    # NAME
    def setName(self, newName: str):
        '''
        Setter function for name of Timed Transition.
        @param newName: Unique new name for Timed Transition, must be string
        '''
        if (checkName(newName)):
            self.name = newName
        else:
            raise Exception(
                "A Timed Transition already exists named: " + newName)

    def getName(self):
        '''
        Getter function for name of Timed Transition.
        Returns current name of Timed Transition.
        '''
        return self.name

    # DIST TYPE
    def setDistType(self, distType):
        '''
        Setter function for distribution type of Timed Transition.
        @param distType: New distribution type value for Timed Transition, must be chosen from predetermined enumeration
        '''
        self.distType = distType

    def getDistType(self):
        '''
        Getter function for distribution type of Timed Transition.
        Returns current distribution type of Timed Transition.
        '''
        return self.distType

    # AGE POLICY
    def setAgePolicy(self, agePolicy):
        '''
        Setter function for age policy to able/disable race age of Timed Transition.
        @param agePolicy: New age policy of Timed Transition, must be chosen from predetermined enumeration.
        '''
        self.agePolicy = agePolicy

    def getAgePolicy(self):
        '''
        Getter function for age policy of Timed Transition.
        Returns current age policy of Timed Transition.
        '''
        return self.agePolicy

    # GUARD
    def setGuard(self, guard: str):
        '''
        Setter function for guard condition of Timed Transition.
        @param guard: New guard condition for Timed Transition to enable firing, must be assessable logic statement in string, i.e. "Queue.tokens >= 1"
        '''
        if(guard is not None):
            try:
                eval(guard)
            except:
                raise Exception(
                    "The guard condition set for Timed Transition must be valid")
            else:
                self.guard = guard
        else:
            self.guard = guard

    def getGuard(self):
        '''
        Getter function for guard condition of Timed Transition.
        Returns current guard condition of Timed Transition.
        '''
        return self.guard

    # FIRE COUNT
    def setFireCount(self, fireCount: int):
        '''
        Setter function for fire count of Timed Transition.
        @param fireCount: New fire count for Timed Transition, must be integer
        '''
        self.fireCount = fireCount

    def getFireCount(self):
        '''
        Getter function for fire count of Timed Transition.
        Returns current fire count of Timed Transition.
        '''
        return self.fireCount

    # INPUT ARCS
    def setInputArcs(self, *inputArcList):
        '''
        Setter function to overwrite Input Arcs targeting current Timed Transition.
        Note: this function deletes existing list of Input Arcs, and creates new list with the given Input Arcs. To add single new Input Arc to Timed Transition's Input Arc list, use addInputArc.
        @param *inputArcList: New tuple of Input Arcs to be added to Timed Transition's Input Arc list, must be a tuple of instances of class Input Arc
        '''
        for arc in inputArcList:
            if(checkType(arc) != "InputArc"):
                raise Exception(
                    "Timed Transition's new Input Arc list's elements must be instances of class Input Arc")
        self.inputArcs.clear
        for arc in inputArcList:
            arc.setToTrans(self)
            self.inputArcs.append(arc)

    def getInputArcs(self):
        '''
        Getter function for list of Input Arcs targeting current Timed Transition.
        Returns current list of Input Arcs targeting current Timed Transition.
        '''
        return self.inputArcs

    def addInputArc(self, newInputArc):
        '''
        Setter function to add new Input Arc targeting current Timed Transition, to Timed Transition's Input Arc list.
        Note: this function adds one new Input Arc to the Timed Transition's Input Arc list. To overwrite the list with a tuple of multiple Input Arcs, use setInputArcs.
        @param newInputArc: New Input Arc to be added to Timed Transition's Input Arc list, must be instance of class Input Arc
        '''
        if(checkType(newInputArc) != "InputArc"):
            raise Exception(
                "Timed Transition's new Input Arc must be instance of class Input Arc")
        newInputArc.setToTrans(self)
        self.inputArcs.append(newInputArc)

    # OUTPUT ARCS
    def setOutputArcs(self, *outputArcList):
        '''
        Setter function to overwrite Output Arcs originating from current Timed Transition.
        Note: this function deletes existing list of Output Arcs, and creates new list with the given Output Arcs. To add single new Output Arc to Timed Transition's Output Arc list, use addOutputArc.
        @param *outputArcList: New tuple of Output Arcs to be added to Timed Transition's Output Arc list, must be a tuple of instances of class Output Arc
        '''
        for arc in outputArcList:
            if(checkType(arc) != "OutputArc"):
                raise Exception(
                    "Timed Transition's new Output Arc list's elements must be instances of class Output Arc")
        self.outputArcs.clear
        for arc in outputArcList:
            arc.setFromTrans(self)
            self.outputArcs.append(arc)

    def getOutputArcs(self):
        '''
        Getter function for list of Output Arcs originating from current Timed Transition.
        Returns current list of Output Arcs originating from current Timed Transition.
        '''
        return self.outputArcs

    def addOutputArc(self, newOutputArc):
        '''
        Setter function to add new Output Arc originating from current Timed Transition, to Timed Transition's Output Arc list.
        Note: this function adds one new Output Arc to the Timed Transition's Output Arc list. To overwrite the list with a tuple of multiple Output Arcs, use setOutputArcs.
        @param newOutputArc: New Output Arc to be added to Timed Transition's Output Arc list, must be instance of class Output Arc
        '''
        if(checkType(newOutputArc) != "OutputArc"):
            raise Exception(
                "Timed Transition's new Output Arc must be instance of class Output Arc")
        newOutputArc.setFromTrans(self)
        self.outputArcs.append(newOutputArc)

    # INHIB ARCS
    def setInhibArcs(self, *inhibArcList):
        '''
        Setter function to overwrite Inhibitor Arcs targeting current Timed Transition.
        Note: this function deletes existing list of Inhibitor Arcs, and creates new list with the given Inhibitor Arcs. To add single new Inhibitor Arc to Timed Transition's Inhibitor Arc list, use addInhibArc.
        @param *inhibArcList: New tuple of Inhibitor Arcs to be added to Timed Transition's Inhibitor Arc list, must be a tuple of instances of class Inhibitor Arc
        '''
        for arc in inhibArcList:
            if(checkType(arc) != "InhibArc"):
                raise Exception(
                    "Timed Transition's new Inhibitor Arc list's elements must be instances of class Inhibitor Arc")
        self.inhibArcs.clear
        for arc in inhibArcList:
            arc.setTarget(self)
            self.inhibArcs.append(arc)

    def getInhibArcs(self):
        '''
        Getter function for list of Inhibitor Arcs targeting current Timed Transition.
        Returns current list of Inhibitor Arcs targeting current Timed Transition.
        '''
        return self.inhibArcs

    def addInhibArc(self, newInhibArc):
        '''
        Setter function to add new Inhibitor Arc targeting current Timed Transition, to Timed Transition's Inhibitor Arc list.
        Note: this function adds one new Inhibitor Arc to the Timed Transition's Inhibitor Arc list. To overwrite the list with a tuple of multiple Inhibitor Arcs, use setInhibArcs.
        @param newInhibArc: New Inhibitor Arc to be added to Timed Transition's Inhibitor Arc list, must be instance of class Inhibitor Arc
        '''
        if(checkType(newInhibArc) != "InhibArc"):
            raise Exception(
                "Timed Transition's new Inhibitor Arc must be instance of class Inhibitor Arc")
        newInhibArc.setTarget(self)
        self.inhibArcs.append(newInhibArc)


def checkName(name):
    for trans in timedTransList:
        if (trans.name == name):
            return False
    return True


def findTransitionByName(name):
    for trans in timedTransList:
        if (trans.name == name):
            return trans
    raise Exception('A Timed Transition does not exists with name: ' + name)


def checkType(object):
    return object.__class__.__name__
