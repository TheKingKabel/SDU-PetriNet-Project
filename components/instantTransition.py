from main import instantTransList

class InstantTransition:

    def __init__(self, name: str, guard: str = None, start: bool = False, enabled: bool = True, fireProbability: float = 1.0, fireCount: int = 0):
        '''
        Create an instance of the Instant Transition class.
        @param name: Unique name of the Instant Transition, must be string
        @param guard: Condition for Instant Transition to be anabled for firing, must be assessable logic statement in string, i.e. "Queue.tokens >= 1"
        @param start: Variable used to mark starting point of Petri Net, must be boolean                TODO: implement PN net / chain depth detection?
        @param enabled: Variable used to update enabled status of Instant Transition, must be boolean    TODO: remove from constructor, it's updated automatically
        @param fireProbability: Variable used to calculate firing probability, must be float
        @param fireCount: Variable used to count the number of firings of Immediate Transition for statistics, must be integer
        '''
        if (checkName(name)):
            self.name = name                        # name of the immediate transition
            if(guard is not None):
                try:
                    eval(guard)
                except:
                    del self
                    raise Exception("The guard function added to Immediate Transition named: " + name + " is invalid")
                else:
                    self.guard = guard              # set guard function
            else:
                self.guard = guard                  # guard is not specified
            self.start = start                      # mark starting point of PN net
            self.enabled = enabled                  # immediate transition enabled for firing, default: true
            self.fireProbability = fireProbability  # probability of firing, default 1.0 (100%)
            self.fireCount = fireCount              # number of times immediate transition has fired, default 0
            
            self.inBoundInputArcs = []              # list of inbound input arcs targeting current immediate transition
            self.outBoundOutputArcs = []            # list of outbound output arcs originating from current immediate transition
            self.outBoundInhibArcs = []             # list of outbound inhibitor arcs originating from current immediate transition
            self.inBoundInhibArcs = []              # list of inbound inhibitor arcs targeting the current immediate transition

            #TODO: other arguments?

            instantTransList.append(self)

        else:
            del self
            raise Exception("An Immediate Transition already exists named: " + name)

    def __str__(self):
        '''
        Default return value of class, gives description of current state of Imeediate Transition.
        '''
        returnString = (
            f"Immediate Transition (name={self.name}, "
            f"starting transition={self.start}, "
            f"with guard function={self.guard}, "
            f"currently enabled={self.enabled}, "
            f"firing probability={self.fireProbability}, "
            f"times fired={self.fireCount}, "
            f"list of inbound input arcs={str(self.inBoundInputArcs)}, "
            f"list of outbound output arcs={str(self.outBoundOutputArcs)}, "
            f"list of inbound inhibitor arcs={str(self.inBoundInhibArcs)}, "
            f"list of outbound inhibitor arcs={str(self.outBoundInhibArcs)}, "
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
            raise Exception("An Immediate Transition already exists named: " + newName)

    def getName(self):
        '''
        Getter function for name of Immediate Transition.
        Returns current name of Immediate Transition.
        '''
        return self.name

    # ENABLE
    def setEnable(self, enabled: bool):
        '''
        Setter function for enable variable of Immediate Transition.
        @param enabled: New value for enable variable of Immediate Transition, must be boolean
        Note: value is dynamically updated during simulation.
        '''
        self.enabled = enabled

    def getEnable(self):
        '''
        Getter function for enable variable of Immediate Transition.
        Returns current enable variable of Immediate Transition.
        '''
        return self.enabled

    # START
    def setStart(self, start: bool):
        '''
        Setter function for start variable of Immediate Transition.
        @param start: New value for start variable of Immediate Transition, must be boolean
        '''
        self.start = start

    def getStart(self):
        '''
        Getter function for start variable of Immediate Transition.
        Returns current start variable of Immediate Transition.
        '''
        return self.start

    # GUARD
    def setGuard(self, guard: str):
        '''
        Setter function for guard condition of Immediate Transition.
        @param guard: New guard condition for Immediate Transition to be abled for firing, must be assessable logic statement in string, i.e. "Queue.tokens >= 1"
        '''
        if(guard is not None):
            try:
                eval(guard)
            except:
                raise Exception("The guard condition set for Immediate Transition must be valid")
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

    # INBOUND INPUT ARCS
    def setInBoundInputArcs(self, *inBoundInputArcList):
        '''
        Setter function to overwrite inbound input arcs targeting current Immediate Transition.
        Note: this function deletes existing list of inbound input arcs, and creates new list with the given parameters. To add single new Input Arc to Immediate Transition's inbound Input Arc list, use addInBoundInputArcs.
        @param *inBoundInputArcList: New tuple of Input Arcs to be added to Immediate Transition's inbound Input Arc list, must be a tuple of instances of class Input Arc
        '''
        for arc in inBoundInputArcList:
            if(checkType(arc) != "InputArc"):
                raise Exception("Immediate Transition's new inbound Input Arc list's elements must be instances of class Input Arc")
        self.inBoundInputArcs.clear
        for arc in inBoundInputArcList:
            arc.setToTrans(self)
            self.inBoundInputArcs.append(arc)
    
    def getInBoundInputArcs(self):
        '''
        Getter function for list of inbound input arcs targeting current Immediate Transition.
        Returns current list of inbound input arcs targeting current Immediate Transition.
        '''
        return self.inBoundInputArcs

    def addInBoundInputArcs(self, newInBoundInputArc):
        '''
        Setter function to add new inbound input arc targeting current Immediate Transition, to Immediate Transition's inbound Input Arc list.
        Note: this function adds one new Input Arc to the Immediate Transition's inbound Input Arc list. To overwrite the list with a tuple of multiple Input Arcs, use setInBoundInputArcs.
        @param newInBoundInputArc: New Input Arc to be added to Immediate Transition's inbound Input Arc list, must be instance of class Input Arc
        '''
        if(checkType(newInBoundInputArc) != "InputArc"):
            raise Exception("Immediate Transition's new inbound Input Arc must be instance of class Input Arc")
        newInBoundInputArc.setToTrans(self)
        self.inBoundInputArcs.append(newInBoundInputArc)
    
    # OUTBOUND OUTPUT ARCS
    def setOutBoundOutputArcs(self, *outBoundOutputArcList):
        '''
        Setter function to overwrite outbound output arcs originating from current Immediate Transition.
        Note: this function deletes existing list of outbound output arcs, and creates new list with the given parameters. To add single new Output Arc to Immediate Transition's outbound Output Arc list, use addOutBoundOutputArcs.
        @param *outBoundOutputArcList: New tuple of Output Arcs to be added to Immediate Transition's outbound Output Arc list, must be a tuple of instances of class Output Arc
        '''
        for arc in outBoundOutputArcList:
            if(checkType(arc) != "OutputArc"):
                raise Exception("Immediate Transition's new outbound Output Arc list's elements must be instances of class Output Arc")
        self.outBoundOutputArcs.clear
        for arc in outBoundOutputArcList:
            arc.setFromTrans(self)
            self.outBoundOutputArcs.append(arc)
    
    def getOutBoundOutputArcs(self):
        '''
        Getter function for list of outbound output arcs originating from current Immediate Transition.
        Returns current list of outbound output arcs originating from current Immediate Transition.
        '''
        return self.outBoundOutputArcs

    def addOutBoundOutputArcs(self, newOutBoundOutputArc):
        '''
        Setter function to add new outbound output arc originating from current Immediate Transition, to Immediate Transition's outbound Output Arc list.
        Note: this function adds one new Output Arc to the Immediate Transition's outbound Output Arc list. To overwrite the list with a tuple of multiple Output Arcs, use setOutBoundOutputArcs.
        @param newOutBoundOutputArc: New Output Arc to be added to Immediate Transition's outbound Output Arc list, must be instance of class Output Arc
        '''
        if(checkType(newOutBoundOutputArc) != "OutputArc"):
            raise Exception("Immediate Transition's new outbound Output Arc must be instance of class Output Arc")
        newOutBoundOutputArc.setFromTrans(self)
        self.outBoundOutputArcs.append(newOutBoundOutputArc)

    # OUTBOUND INHIB ARCS
    def setOutBoundInhibArcs(self, *outBoundInhibArcList):
        '''
        Setter function to overwrite outbound inhibitor arcs originating from current Immediate Transition.
        Note: this function deletes existing list of outbound inhibitor arcs, and creates new list with the given parameters. To add single new Inhibitor Arc to Immediate Transition's outbound Inhibitor Arc list, use addOutBoundInhibArcs.
        @param *outBoundInhibArcList: New tuple of Inhibitor Arcs to be added to Immediate Transition's outbound Inhibitor Arc list, must be a tuple of instances of class Inhibitor Arc
        '''
        for arc in outBoundInhibArcList:
            if(checkType(arc) != "InhibArc"):
                raise Exception("Immediate Transition's new outbound Inhibitor Arc list's elements must be instances of class Inhibitor Arc")
        self.outBoundInhibArcs.clear
        for arc in outBoundInhibArcList:
            arc.setOrigin(self)
            self.outBoundInhibArcs.append(arc)
    
    def getOutBoundInhibArcs(self):
        '''
        Getter function for list of outbound inhibitor arcs originating from current Immediate Transition.
        Returns current list of outbound inhibitor arcs originating from current Immediate Transition.
        '''
        return self.outBoundInhibArcs

    def addOutBoundInhibArcs(self, newOutBoundInhibArc):
        '''
        Setter function to add new outbound inhibitor arc originating from current Immediate Transition, to Immediate Transition's outbound Inhibitor Arc list.
        Note: this function adds one new Inhibitor Arc to the Immediate Transition's outbound Inhibitor Arc list. To overwrite the list with a tuple of multiple Inhibitor Arcs, use setOutBoundInhibArcs.
        @param newOutBoundInhibArc: New Inhibitor Arc to be added to Immediate Transition's outbound Inhibitor Arc list, must be instance of class Inhibitor Arc
        '''
        if(checkType(newOutBoundInhibArc) != "InhibArc"):
            raise Exception("Immediate Transition's new outbound Inhibitor Arc must be instance of class Inhibitor Arc")
        newOutBoundInhibArc.setOrigin(self)
        self.outBoundInhibArcs.append(newOutBoundInhibArc)

    # INBOUND INHIB ARCS
    def setInBoundInhibArcs(self, *inBoundInhibArcList):
        '''
        Setter function to overwrite inbound inhibitor arcs targeting current Immediate Transition.
        Note: this function deletes existing list of inbound inhibitor arcs, and creates new list with the given parameters. To add single new Inhibitor Arc to Immediate Transition's inbound Inhibitor Arc list, use addInBoundInhibArcs.
        @param *inBoundInhibArcList: New tuple of Inhibitor Arcs to be added to Immediate Transition's inbound Inhibitor Arc list, must be a tuple of instances of class Inhibitor Arc
        '''
        for arc in inBoundInhibArcList:
            if(checkType(arc) != "InhibArc"):
                raise Exception("Immediate Transition's new inbound Inhibitor Arc list's elements must be instances of class Inhibitor Arc")
        self.inBoundInhibArcs.clear
        for arc in inBoundInhibArcList:
            arc.setTarget(self)
            self.inBoundInhibArcs.append(arc)
    
    def getInBoundInhibArcs(self):
        '''
        Getter function for list of inbound inhibitor arcs targeting current Immediate Transition.
        Returns current list of inbound inhibitor arcs targeting current Immediate Transition.
        '''
        return self.inBoundInhibArcs

    def addInBoundInhibArcs(self, newInBoundInhibArc):
        '''
        Setter function to add new inbound inhibitor arc targeting current Immediate Transition, to Immediate Transition's inbound Inhibitor Arc list.
        Note: this function adds one new Inhibitor Arc to the Immediate Transition's inbound Inhibitor Arc list. To overwrite the list with a tuple of multiple Inhibitor Arcs, use setInBoundInhibArcs.
        @param newInBoundInhibArc: New Inhibitor Arc to be added to Immediate Transition's inbound Inhibitor Arc list, must be instance of class Inhibitor Arc
        '''
        if(checkType(newInBoundInhibArc) != "InhibArc"):
            raise Exception("Immediate Transition's new inbound Inhibitor Arc must be instance of class Inhibitor Arc")
        newInBoundInhibArc.setTarget(self)
        self.inBoundInhibArcs.append(newInBoundInhibArc)

def checkName(name):
    for trans in instantTransList:
        if (trans.name == name):
            return False
    return True

def findTransitionByName(name):
    for trans in instantTransList:
        if (trans.name == name):
            return trans
    raise Exception('An Immediate Transition does not exists with name: ' + name)

def checkType(object):
    return object.__class__.__name__


# def setName(transName: str, newName: str):
#     trans = findTransitionByName(transName)
#     if (checkName(newName)):
#         trans.name = newName
#     else:
#         raise Exception("An Immediate Transition already exists named: " + newName)

# def getName(transName: str):
#     trans = findTransitionByName(transName)
#     return trans.name

# def setEnabled(transName: str, enabled: bool):
#     trans = findTransitionByName(transName)
#     trans.enabled = enabled

# def getEnabled(transName: str):
#     trans = findTransitionByName(transName)
#     return trans.enabled

# def setFireProbability(transName: str, fireProbability: float):
#     trans = findTransitionByName(transName)
#     trans.fireProbability = fireProbability

# def getFireProbability(transName: str, fireProbability: float):
#     trans = findTransitionByName(transName)
#     trans.fireProbability = fireProbability

# def setFireCount(transName: str, fireCount: int):
#     trans = findTransitionByName(transName)
#     trans.fireCount = fireCount

# def getFireCount(transName: str):
#     trans = findTransitionByName(transName)
#     return trans.fireCount