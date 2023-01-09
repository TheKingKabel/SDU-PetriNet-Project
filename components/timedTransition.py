from main import timedTransList

class TimedTransition:

    def __init__(self, name: str, distType, agePolicy, start: bool = False, enabled: bool = True, fireCount: int = 0):
        '''
        Create an instance of the Timed Transition class.
        @param name: Unique name of the Timed Transition, must be string
        @param distType: Distribution type of random firings of the Timed Transition, must be chosen from predetermined enumeration         TODO: implement enumeration, define default
        @param agePolicy: Setting to able/disable race age of Timed Transition, must be chosen from predetermined enumeration               TODO: implement enumeration, define default
        @param start: Variable used to mark starting point of Petri Net, must be boolean                                                    TODO: implement PN net / chain depth detection?
        @param enabled: Variable used to update enabled status of Timed Transition, must be boolean                                         TODO: remove from constructor, it's updated automatically
        @param fireCount: Variable used to count the number of firings of Timed Transition for statistics, must be integer
        '''
        if (checkName(name)):
            self.name = name                                                                        # name of the timed transition
            self.distType = distType                                                                # type of distribution                  TODO: implement, check type?
            self.enabled = enabled                                                                  # transition enabled for firing, default: true
            self.agePolicy = agePolicy                                                              # age policy setting of transition      TODO: implement race anabled/disabled, check type?
            self.fireCount = fireCount                                                              # number of times transition has fired, default 0
            self.start = start                                                                      # mark starting point of PN net

            self.outBoundOutputArcs = []                                                            # list of outbound output arcs originating from current timed transition
            self.inBoundInputArcs = []                                                              # list of inbound input arcs targeting the current timed transition
            self.outBoundInhibArcs = []                                                             # list of outbound inhibitor arcs originating from current timed transition
            self.inBoundInhibArcs = []                                                              # list of inbound inhibitor arcs targeting the current timed transition

            #TODO: other arguments?

            timedTransList.append(self)

        else:
            del self
            raise Exception("A Timed Transition already exists named: " + name)

    def __str__(self):
        '''
        Default return value of class, gives description of current state of Timed Transition.
        '''
        return f'Timed Transition (name={self.name}, distribution type={self.distType}, enabled={self.enabled}, times fired={self.fireCount}'

    # NAME
    def setName(self, newName: str):
        '''
        Setter function for name of Timed Transition.
        @param newName: Unique new name for Timed Transition, must be string
        '''
        if (checkName(newName)):
            self.name = newName
        else:
            raise Exception("A Timed Transition already exists named: " + newName)

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

    # ENABLE
    def setEnable(self, enabled: bool):
        '''
        Setter function for enable variable of Timed Transition.
        @param enabled: New value for enable variable of Timed Transition, must be boolean
        Note: value is dynamically updated during simulation.
        '''
        self.enabled = enabled

    def getEnable(self):
        '''
        Getter function for enable variable of Timed Transition.
        Returns current enable variable of Timed Transition.
        '''
        return self.enabled

    # START
    def setStart(self, start: bool):
        '''
        Setter function for start variable of Timed Transition.
        @param start: New value for start variable of Timed Transition, must be boolean
        '''
        self.start = start

    def getStart(self):
        '''
        Getter function for start variable of Timed Transition.
        Returns current start variable of Timed Transition.
        '''
        return self.start

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

    # INBOUND INPUT ARCS
    def setInBoundInputArcs(self, *inBoundInputArcList):
        '''
        Setter function to overwrite inbound input arcs targeting current Timed Transition.
        Note: this function deletes existing list of inbound input arcs, and creates new list with the given parameters. To add single new Input Arc to Timed Transition's inbound Input Arc list, use addInBoundInputArcs.
        @param *inBoundInputArcList: New tuple of Input Arcs to be added to Timed Transition's inbound Input Arc list, must be a tuple of instances of class Input Arc
        '''
        for arc in inBoundInputArcList:
            if(checkType(arc) != "InputArc"):
                raise Exception("Timed Transition's new inbound Input Arc list's elements must be instances of class Input Arc")
        self.inBoundInputArcs.clear
        for arc in inBoundInputArcList:
            arc.setToTrans(self)
            self.inBoundInputArcs.append(arc)
    
    def getInBoundInputArcs(self):
        '''
        Getter function for list of inbound input arcs targeting current Timed Transition.
        Returns current list of inbound input arcs targeting current Timed Transition.
        '''
        return self.inBoundInputArcs

    def addInBoundInputArcs(self, newInBoundInputArc):
        '''
        Setter function to add new inbound input arc targeting current Timed Transition, to Timed Transition's inbound Input Arc list.
        Note: this function adds one new Input Arc to the Timed Transition's inbound Input Arc list. To overwrite the list with a tuple of multiple Input Arcs, use setInBoundInputArcs.
        @param newInBoundInputArc: New Input Arc to be added to Timed Transition's inbound Input Arc list, must be instance of class Input Arc
        '''
        if(checkType(newInBoundInputArc) != "InputArc"):
            raise Exception("Timed Transition's new inbound Input Arc must be instance of class Input Arc")
        newInBoundInputArc.setToTrans(self)
        self.inBoundInputArcs.append(newInBoundInputArc)
    
    # OUTBOUND OUTPUT ARCS
    def setOutBoundOutputArcs(self, *outBoundOutputArcList):
        '''
        Setter function to overwrite outbound output arcs originating from current Timed Transition.
        Note: this function deletes existing list of outbound output arcs, and creates new list with the given parameters. To add single new Output Arc to Timed Transition's outbound Output Arc list, use addOutBoundOutputArcs.
        @param *outBoundOutputArcList: New tuple of Output Arcs to be added to Timed Transition's outbound Output Arc list, must be a tuple of instances of class Output Arc
        '''
        for arc in outBoundOutputArcList:
            if(checkType(arc) != "OutputArc"):
                raise Exception("Timed Transition's new outbound Output Arc list's elements must be instances of class Output Arc")
        self.outBoundOutputArcs.clear
        for arc in outBoundOutputArcList:
            arc.setFromTrans(self)
            self.outBoundOutputArcs.append(arc)
    
    def getOutBoundOutputArcs(self):
        '''
        Getter function for list of outbound output arcs originating from current Timed Transition.
        Returns current list of outbound output arcs originating from current Timed Transition.
        '''
        return self.outBoundOutputArcs

    def addOutBoundOutputArcs(self, newOutBoundOutputArc):
        '''
        Setter function to add new outbound output arc originating from current Timed Transition, to Timed Transition's outbound Output Arc list.
        Note: this function adds one new Output Arc to the Timed Transition's outbound Output Arc list. To overwrite the list with a tuple of multiple Output Arcs, use setOutBoundOutputArcs.
        @param newOutBoundOutputArc: New Output Arc to be added to Timed Transition's outbound Output Arc list, must be instance of class Output Arc
        '''
        if(checkType(newOutBoundOutputArc) != "OutputArc"):
            raise Exception("Timed Transition's new outbound Output Arc must be instance of class Output Arc")
        newOutBoundOutputArc.setFromTrans(self)
        self.outBoundOutputArcs.append(newOutBoundOutputArc)

    # OUTBOUND INHIB ARCS
    def setOutBoundInhibArcs(self, *outBoundInhibArcList):
        '''
        Setter function to overwrite outbound inhibitor arcs originating from current Timed Transition.
        Note: this function deletes existing list of outbound inhibitor arcs, and creates new list with the given parameters. To add single new Inhibitor Arc to Timed Transition's outbound Inhibitor Arc list, use addOutBoundInhibArcs.
        @param *outBoundInhibArcList: New tuple of Inhibitor Arcs to be added to Timed Transition's outbound Inhibitor Arc list, must be a tuple of instances of class Inhibitor Arc
        '''
        for arc in outBoundInhibArcList:
            if(checkType(arc) != "InhibArc"):
                raise Exception("Timed Transition's new outbound Inhibitor Arc list's elements must be instances of class Inhibitor Arc")
        self.outBoundInhibArcs.clear
        for arc in outBoundInhibArcList:
            arc.setOrigin(self)
            self.outBoundInhibArcs.append(arc)
    
    def getOutBoundInhibArcs(self):
        '''
        Getter function for list of outbound inhibitor arcs originating from current Timed Transition.
        Returns current list of outbound inhibitor arcs originating from current Timed Transition.
        '''
        return self.outBoundInhibArcs

    def addOutBoundInhibArcs(self, newOutBoundInhibArc):
        '''
        Setter function to add new outbound inhibitor arc originating from current Timed Transition, to Timed Transition's outbound Inhibitor Arc list.
        Note: this function adds one new Inhibitor Arc to the Timed Transition's outbound Inhibitor Arc list. To overwrite the list with a tuple of multiple Inhibitor Arcs, use setOutBoundInhibArcs.
        @param newOutBoundInhibArc: New Inhibitor Arc to be added to Timed Transition's outbound Inhibitor Arc list, must be instance of class Inhibitor Arc
        '''
        if(checkType(newOutBoundInhibArc) != "InhibArc"):
            raise Exception("Timed Transition's new outbound Inhibitor Arc must be instance of class Inhibitor Arc")
        newOutBoundInhibArc.setOrigin(self)
        self.outBoundInhibArcs.append(newOutBoundInhibArc)

    # INBOUND INHIB ARCS
    def setInBoundInhibArcs(self, *inBoundInhibArcList):
        '''
        Setter function to overwrite inbound inhibitor arcs targeting current Timed Transition.
        Note: this function deletes existing list of inbound inhibitor arcs, and creates new list with the given parameters. To add single new Inhibitor Arc to Timed Transition's inbound Inhibitor Arc list, use addInBoundInhibArcs.
        @param *inBoundInhibArcList: New tuple of Inhibitor Arcs to be added to Timed Transition's inbound Inhibitor Arc list, must be a tuple of instances of class Inhibitor Arc
        '''
        for arc in inBoundInhibArcList:
            if(checkType(arc) != "InhibArc"):
                raise Exception("Timed Transition's new inbound Inhibitor Arc list's elements must be instances of class Inhibitor Arc")
        self.inBoundInhibArcs.clear
        for arc in inBoundInhibArcList:
            arc.setTarget(self)
            self.inBoundInhibArcs.append(arc)
    
    def getInBoundInhibArcs(self):
        '''
        Getter function for list of inbound inhibitor arcs targeting current Timed Transition.
        Returns current list of inbound inhibitor arcs targeting current Timed Transition.
        '''
        return self.inBoundInhibArcs

    def addInBoundInhibArcs(self, newInBoundInhibArc):
        '''
        Setter function to add new inbound inhibitor arc targeting current Timed Transition, to Timed Transition's inbound Inhibitor Arc list.
        Note: this function adds one new Inhibitor Arc to the Timed Transition's inbound Inhibitor Arc list. To overwrite the list with a tuple of multiple Inhibitor Arcs, use setInBoundInhibArcs.
        @param newInBoundInhibArc: New Inhibitor Arc to be added to Timed Transition's inbound Inhibitor Arc list, must be instance of class Inhibitor Arc
        '''
        if(checkType(newInBoundInhibArc) != "InhibArc"):
            raise Exception("Timed Transition's new inbound Inhibitor Arc must be instance of class Inhibitor Arc")
        newInBoundInhibArc.setTarget(self)
        self.inBoundInhibArcs.append(newInBoundInhibArc)
    

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


def setName(transName: str, newName: str):
    trans = findTransitionByName(transName)
    if (checkName(newName)):
        trans.name = newName
    else:
        raise Exception("A Timed Transition already exists named: " + newName)

def checkType(object):
    return object.__class__.__name__


# def getName(transName: str):
#     trans = findTransitionByName(transName)
#     return trans.name
    
# def setDistType(transName: str, distType):
#     trans = findTransitionByName(transName)
#     trans.distType = distType

# def getDistType(transName: str):
#     trans = findTransitionByName(transName)
#     return trans.distType

# def setAgePolicy(transName: str, agePolicy):
#     trans = findTransitionByName(transName)
#     trans.agePolicy = agePolicy

# def getAgePolicy(transName: str):
#     trans = findTransitionByName(transName)
#     return trans.agePolicy

# def setEnabled(transName: str, enabled: bool):
#     trans = findTransitionByName(transName)
#     trans.enabled = enabled

# def getEnabled(transName: str):
#     trans = findTransitionByName(transName)
#     return trans.enabled

# def setFireCount(transName: str, fireCount: int):
#     trans = findTransitionByName(transName)
#     trans.fireCount = fireCount

# def getFireCount(transName: str):
#     trans = findTransitionByName(transName)
#     return trans.fireCount