from definitions.distribution_types import DistributionType
from definitions.agepolicy_types import AgePolicyType
from definitions.timeunit_types import TimeUnitType


class TimedTransition:

    def __init__(self, name: str, petriNet, distType: DistributionType = 'NORM', distArgA: float = 0.0, distArgB: float = 1.0, distArgC: float = 0.0, distArgD: float = 0.0, timeUnitType: TimeUnitType = 'sec', agePolicy: AgePolicyType = 'R_ENABLE', guard=None, fireCount: int = 0):
        '''
        Create an instance of the Timed Transition class.
        @param name: Name of the Timed Transition, must be string, must be unique in assigned Petri Net
        @param petriNet: Reference of parent Petri Net element for Timed Transition to be assigned to, must be instance of class PetriNet
        @param distType: Distribution type of random firings of the Timed Transition, must be chosen from predetermined enumeration         TODO: implement enumeration, define default
        @param agePolicy: Setting to able/disable race age of Timed Transition, must be chosen from predetermined enumeration               TODO: implement enumeration, define default
        @param guard: Condition for Timed Transition to be enabled for firing, must be assessable logic statement in string, i.e. "Queue.tokens >= 1"
        @param fireCount: Variable used to count the number of firings of Timed Transition for statistics, must be integer
        '''
        if(checkType(petriNet) == "PetriNet"):
            # reference of Petri Net consisting current Timed Transition
            self.petriNet = petriNet

            if (checkName(petriNet, name)):
                # name of the Timed Transition
                self.name = name

                # type of distribution
                disTypes = [member.name for member in DistributionType]

                if(distType in disTypes):
                    self.distType = distType
                else:
                    del self
                    returnMsg = "The distribution type set for Timed Transition named: " + \
                        name + " is not defined.\nSupported distribution types: "
                    for member in DistributionType:
                        returnMsg += '[' + member.name + \
                            ": " + member.value + '], '
                    raise Exception(
                        returnMsg
                    )

                # time unit setting of transition
                timeTypes = [member.name for member in TimeUnitType]

                if(timeUnitType in timeTypes):
                    self.timeUnitType = timeUnitType
                else:
                    del self
                    returnMsg = "The time unit type set for Timed Transition named: " + \
                        name + " is not defined.\nSupported time unit types: "
                    for member in TimeUnitType:
                        returnMsg += '[' + member.name + \
                            ": " + member.value + '], '
                    raise Exception(
                        returnMsg
                    )

                # age policy setting of transition
                agePolicies = [member.name for member in AgePolicyType]

                if(agePolicy in agePolicies):
                    self.agePolicy = agePolicy
                else:
                    del self
                    returnMsg = "The age policy set for Timed Transition named: " + \
                        name + " is not defined.\nSupported age policies: "
                    for member in agePolicies:
                        returnMsg += '[' + member.name + \
                            ": " + member.value + '], '
                    raise Exception(
                        returnMsg
                    )

                # set guard function if correctly specified, set to None if not applicable
                if(guard is not None):
                    if(checkType(guard()) == 'bool'):
                        # set guard function
                        self.guard = guard
                    else:
                        del self
                        raise Exception(
                            "The guard function added to Timed Transition named: " + name + " is invalid")
                else:
                    # guard is not specified
                    self.guard = None

                # number of times Timed Transition has fired, default 0
                self.fireCount = fireCount

                # previous number of times Timed Transition has fired, initially same value as fireCount
                self.prevFireCount = fireCount

                # Timed Transition enabled for firing, default: False, to be overwritten during simulation
                self.enabled = False

                # Delay for next firing, automatically generated during simulation, default None, if no enabled set to None
                self.delay = None

                # Distribution arguments TODO: change default value?
                self.a = distArgA
                self.b = distArgB
                self.c = distArgC
                self.d = distArgD

                # list of Input Arcs targeting the current Timed Transition
                self.inputArcs = []

                # list of Output Arcs originating from current Timed Transition
                self.outputArcs = []

                # list of inbound Inhibitor Arcs targeting the current Timed Transition
                self.inhibArcs = []

                # add Timed Transition to PN's Timed Transition list
                petriNet.timedTransList.append(self)

            else:
                del self
                raise Exception(
                    "An Timed Transition already exists named: " + name + ", in Petri Net named: " + petriNet.name)

        else:
            del self
            raise Exception(
                "Petri Net with name: " + petriNet + " does not exist!")

    def __str__(self):
        '''
        Default return value of class, gives description of current state of Timed Transition.
        '''
        returnString = (
            f"Timed Transition (name: {self.name}, "
            f"in Petri Net named: {self.petriNet.name}, "
            f"with distribution type: {self.distType}, "
            f"distribution arguments: {self.a}, {self.b}, {self.c}, {self.d}, "
            f"with guard function: {self.guard}, "
            f"currently enabled: {self.enabled}, "
            f"current firing delay: {self.delay}, "
            f"age policy: {self.agePolicy}, "
            f"times fired: {self.fireCount}, "
            "list of targeting Input Arcs: ")
        for arc in self.inputArcs:
            returnString += f"{str(arc)},\n"
        returnString += "list of originating Output Arcs: "
        for arc in self.outputArcs:
            returnString += f"{str(arc)},\n"
        returnString += "list of targeting Inhibitor Arcs: "
        for arc in self.inhibArcs:
            returnString += f"{str(arc)},\n"

        return returnString

    # NAME
    def setName(self, newName: str):
        '''
        Setter function for name of Timed Transition.
        @param newName: New name for Timed Transition, must be string, must be unique in assigned Petri Net
        '''
        if (checkName(self.petriNet, newName)):
            self.name = newName
        else:
            raise Exception(
                "A Timed Transition already exists named: " + newName + ", in Petri Net named: " + self.petriNet.name)

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
        @param guard: New guard condition for Timed Transition to enable firing, must be assessable logic statement in string, i.e. "Queue.tokens >= 1" TODO: please only use references to elements created in the SAME Petri Net class
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
            self.guard = None

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
        @param *inputArcList: New tuple of Input Arcs to be added to Timed Transition's Input Arc list, must be a tuple of instances of class Input Arc, Input Arcs must be assigned to same Petri Net instance
        '''
        for arc in inputArcList:
            if(checkType(arc) != "InputArc"):
                raise Exception(
                    "Timed Transition's new Input Arc list's elements must be instances of class Input Arc")
            if(arc.petriNet != self.petriNet):
                raise Exception(
                    "Timed Transition's new Input Arc list's elements must be assigned to same Petri Net of Timed Transition!")

        # cleanup of old input arcs
        for arc in self.inputArcs:
            # setting reference of their target Transition to None
            arc.toTrans = None

        self.inputArcs.clear()

        # setting new input arcs
        for arc in inputArcList:
            # removing references to arcs from old target's inputArcs list
            if (arc.toTrans is not None):
                arc.toTrans.inputArcs.remove(arc)
            arc.toTrans = self
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
        @param newInputArc: New Input Arc to be added to Timed Transition's Input Arc list, must be instance of class Input Arc, must be assigned to same Petri Net instance
        '''
        if(checkType(newInputArc) != "InputArc"):
            raise Exception(
                "Timed Transition's new Input Arc must be instance of class Input Arc")
        if(newInputArc.petriNet != self.petriNet):
            raise Exception(
                "Timed Transition's new Input Arc must be assigned to same Petri Net of Timed Transition!")

        if (newInputArc.toTrans is not None):
            newInputArc.toTrans.inputArcs.remove(newInputArc)
        newInputArc.toTrans = self
        self.inputArcs.append(newInputArc)

    # OUTPUT ARCS
    def setOutputArcs(self, *outputArcList):
        '''
        Setter function to overwrite Output Arcs originating from current Timed Transition.
        Note: this function deletes existing list of Output Arcs, and creates new list with the given Output Arcs. To add single new Output Arc to Timed Transition's Output Arc list, use addOutputArc.
        @param *outputArcList: New tuple of Output Arcs to be added to Timed Transition's Output Arc list, must be a tuple of instances of class Output Arc, Output Arcs must be assigned to same Petri Net instance
        '''
        for arc in outputArcList:
            if(checkType(arc) != "OutputArc"):
                raise Exception(
                    "Timed Transition's new Output Arc list's elements must be instances of class Output Arc")
            if(arc.petriNet != self.petriNet):
                raise Exception(
                    "Timed Transition's new Output Arc list's elements must be assigned to same Petri Net of Timed Transition!")

        # cleanup of old output arcs
        for arc in self.outputArcs:
            # setting reference of their origin Transition to None
            arc.fromTrans = None

        self.outputArcs.clear()

        # setting new output arcs
        for arc in outputArcList:
            # removing references to arcs from old origin's outputArcs list
            if(arc.fromTrans is not None):
                arc.fromTrans.outputArcs.remove(arc)
            arc.fromTrans = self
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
        @param newOutputArc: New Output Arc to be added to Timed Transition's Output Arc list, must be instance of class Output Arc, must be assigned to same Petri Net instance
        '''
        if(checkType(newOutputArc) != "OutputArc"):
            raise Exception(
                "Timed Transition's new Output Arc must be instance of class Output Arc")
        if(newOutputArc.petriNet != self.petriNet):
            raise Exception(
                "Timed Transition's new Output Arc must be assigned to same Petri Net of Timed Transition!")

        if(newOutputArc.fromTrans is not None):
            newOutputArc.fromTrans.outputArcs.remove(newOutputArc)
        newOutputArc.fromTrans = self
        self.outputArcs.append(newOutputArc)

    # INHIB ARCS
    def setInhibArcs(self, *inhibArcList):
        '''
        Setter function to overwrite Inhibitor Arcs targeting current Timed Transition.
        Note: this function deletes existing list of Inhibitor Arcs, and creates new list with the given Inhibitor Arcs. To add single new Inhibitor Arc to Timed Transition's Inhibitor Arc list, use addInhibArc.
        @param *inhibArcList: New tuple of Inhibitor Arcs to be added to Timed Transition's Inhibitor Arc list, must be a tuple of instances of class Inhibitor Arc, Inhibitor Arcs must be assigned to same Petri Net instance
        '''
        for arc in inhibArcList:
            if(checkType(arc) != "InhibArc"):
                raise Exception(
                    "Timed Transition's new Inhibitor Arc list's elements must be instances of class Inhibitor Arc")
            if(arc.petriNet != self.petriNet):
                raise Exception(
                    "Timed Transition's new Inhibitor Arc list's elements must be assigned to same Petri Net of Timed Transition!")

        # cleanup of old inhib arcs
        for arc in self.inhibArcs:
            # setting reference of their target Transition to None
            arc.target = None

        self.inhibArcs.clear()

        # setting new inhib arcs
        for arc in inhibArcList:
            # removing references to arcs from old target's inhibArcs list
            if(arc.target is not None):
                arc.target.inhibArcs.remove(arc)
            arc.target = self
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
        @param newInhibArc: New Inhibitor Arc to be added to Timed Transition's Inhibitor Arc list, must be instance of class Inhibitor Arc, must be assigned to same Petri Net instance
        '''
        if(checkType(newInhibArc) != "InhibArc"):
            raise Exception(
                "Timed Transition's new Inhibitor Arc must be instance of class Inhibitor Arc")
        if(newInhibArc.petriNet != self.petriNet):
            raise Exception(
                "Timed Transition's new Inhibitor Arc must be assigned to same Petri Net of Timed Transition!")

        if(newInhibArc.target is not None):
            newInhibArc.target.inhibArcs.remove(newInhibArc)
        newInhibArc.target = self
        self.inhibArcs.append(newInhibArc)


def checkName(petriNet, name):
    for trans in petriNet.timedTransList:
        if (trans.name == name):
            return False
    return True


def checkType(object):
    return object.__class__.__name__
