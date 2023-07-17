# components/timedTransition.py module for Petri Net Project
# contains class definition for object type Timed Transition

from definitions.distribution_types import DistributionType
from definitions.agepolicy_types import AgePolicyType
from definitions.timeunit_types import TimeUnitType


class TimedTransition:
    '''
    Class that represents a Timed Transition object.
    '''

    def __init__(self, name: str, petriNet, distType: DistributionType = 'NORM', distArgA: float = 0.0, distArgB: float = 1.0, distArgC: float = 0.0, distArgD: float = 0.0, timeUnitType: TimeUnitType = 'sec', agePolicy: AgePolicyType = 'R_ENABLE', guard=None, fireCount: int = 0):
        '''
        Constructor method of the Timed Transition class.
        Arguments:
            @param name: Name of the Timed Transition, must be string, must be unique amongst Timed Transition names in assigned Petri Net.
            @param petriNet: Reference of parent Petri Net object for Timed Transition to be assigned to, must be instance of class PetriNet.
            @param distType (optional): Distribution type of random firings of the Timed Transition, must be chosen from predefined list. Default value: 'NORM' (Normal distribution).
            @param distArgs*[A, B, C, D] (optional): Distribution type parameters, must be numbers (integer or floating), parameter types depend on chosen distribution type, following same parameter order as in scipy library's sampling function (scipy.stats.<distribution>.rvs), e.g. normal distribution requires distArgA = loc (mean), and distArgB = scale (standard deviation).
            @param timeUnitType (optional): Parameter used to define time unit for Timed Transition's random firings, must be chosen from predefined list. Default value: 'sec' (seconds).
            @param agePolicy (optional): Parameter used enable/disable race age of Timed Transition, must be chosen from predefined list. Default value: 'R_ENABLE' (Race enabled).
            @param guard (optional): Condition for Timed Transition to be enabled for firing, must be reference to a callable function defined in the user file, returning boolean value True or False, i.e. "PetriNet.findPlaceByName("Queue").tokens >= 1". Default value: None.
            @param fireCount (optional): Parameter used to define initial number of firings of Timed Transition, used for statistics, must be integer, must not be smaller than 0. Default value: 0.
        '''

        # Type checks
        if (_checkType(petriNet) == "PetriNet"):
            # set reference of Petri Net to assign current Timed Transition to
            self.petriNet = petriNet

            if (_checkName(petriNet, name)):
                # set name of the Timed Transition
                self.name = str(name)

                # set type of distribution
                disTypes = [member.name for member in DistributionType]

                if (distType in disTypes):
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

                # set time unit of Timed Transition
                timeTypes = [member.name for member in TimeUnitType]

                if (timeUnitType in timeTypes):
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

                # set age policy of Timed Transition
                agePolicies = [member.name for member in AgePolicyType]

                if (agePolicy in agePolicies):
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
                if (guard is not None):
                    if (_checkType(guard()) == 'bool'):
                        # set guard function
                        self.guard = guard
                    else:
                        del self
                        raise Exception(
                            "The guard function added to Timed Transition named: " + name + " is invalid, not returning Boolean value")
                else:
                    # guard is not specified
                    self.guard = None

                # set number of times Timed Transition has fired, default 0
                # fire count must be greater or equal than 0
                if (_checkType(fireCount) == 'int'):
                    if (fireCount < 0):
                        del self
                        raise Exception(
                            "The fireCount parameter of Timed Transition named: " + name + " must not be smaller than 0!")
                    else:
                        self.fireCount = fireCount
                        self.initFireCount = fireCount
                else:
                    del self
                    raise Exception(
                        "The fireCount parameter of Timed Transition named: " + name + " must be an integer number!")

                # set previous number of times Timed Transition has fired, initially same value as fireCount (used for statistics)
                self.prevFireCount = fireCount

                # set if Timed Transition is enabled for firing, default: False, checked and set automatically during simulation
                self.enabled = False

                # set delay for next firing, automatically generated and set during simulation, default None, if not enabled set to None
                self.delay = None

                # Distribution arguments
                # distArgA
                if (_checkType(distArgA) == 'int' or _checkType(distArgA) == 'float'):
                    self.a = distArgA
                else:
                    del self
                    raise Exception("The distribution argument distArgA: " + str(distArgA) +
                                    " in Timed Transition named: " + name + " is invalid, not a number (int or float)")

                # distArgB
                if (_checkType(distArgB) == 'int' or _checkType(distArgB) == 'float'):
                    self.b = distArgB
                else:
                    del self
                    raise Exception("The distribution argument distArgB: " + str(distArgB) +
                                    " in Timed Transition named: " + name + " is invalid, not a number (int or float)")

                # distArgC
                if (_checkType(distArgC) == 'int' or _checkType(distArgC) == 'float'):
                    self.c = distArgC
                else:
                    del self
                    raise Exception("The distribution argument distArgC: " + str(distArgC) +
                                    " in Timed Transition named: " + name + " is invalid, not a number (int or float)")

                # distArgD
                if (_checkType(distArgD) == 'int' or _checkType(distArgD) == 'float'):
                    self.d = distArgD
                else:
                    del self
                    raise Exception("The distribution argument distArgD: " + str(distArgD) +
                                    " in Timed Transition named: " + name + " is invalid, not a number (int or float)")

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
                    "A Timed Transition already exists named: " + name + ", in Petri Net named: " + petriNet.name)

        else:
            del self
            raise Exception(
                "Petri Net with name: " + petriNet + " does not exist!")

    def __str__(self):
        '''
        Returns user-friendly string representation (description) of Timed Transition object.
        '''
        returnString = (
            f"Timed Transition\n"
            f"\tname: {self.name},\n"
            f"\tin Petri Net named: {self.petriNet.name},\n"
            f"\twith guard function: {self.guard},\n"
            f"\twith distribution type: {self.distType},\n"
            f"\tdistribution arguments: {self.a}, {self.b}, {self.c}, {self.d},\n"
            f"\ttime unit: {self.timeUnitType},\n"
            f"\tage policy: {self.agePolicy},\n"
            f"\tcurrent firing times: {self.fireCount},\n"
            f"\tnumber of targeting Input Arcs: {len(self.inputArcs)},\n"
            "\tlist of targeting Input Arcs:\n")
        if (len(self.inputArcs) == 0):
            returnString += '\t\t' + 'None' + '\n'
        else:
            for arc in self.inputArcs:
                returnString += '\t\t' + \
                    '\t\t'.join(str(arc).splitlines(True)) + '\n'
        returnString += f"\tnumber of originating Output Arcs: {len(self.outputArcs)},\n"
        returnString += "\tlist of originating Output Arcs:\n"
        if (len(self.outputArcs) == 0):
            returnString += '\t\t' + 'None' + '\n'
        else:
            for arc in self.outputArcs:
                returnString += '\t\t' + \
                    '\t\t'.join(str(arc).splitlines(True)) + '\n'
        returnString += f"\tnumber of targeting Inhibitor Arcs: {len(self.inhibArcs)},\n"
        returnString += "\tlist of targeting Inhibitor Arcs:\n"
        if (len(self.inhibArcs) == 0):
            returnString += '\t\t' + 'None' + '\n'
        else:
            for arc in self.inhibArcs:
                returnString += '\t\t' + \
                    '\t\t'.join(str(arc).splitlines(True)) + '\n'

        return returnString

    def _resetState(self):
        '''
        Resets the Timed Transition to its initial state after a simulation run.
        '''
        self.fireCount = self.initFireCount
        self.prevFireCount = self.initFireCount
        self.delay = None
        self.competing = False
        self.enabled = False

    # getter-setters
    # NAME

    def setName(self, newName: str):
        '''
        Setter function for name of Timed Transition.
            @param newName: New name for Timed Transition, must be string, must be unique in assigned Petri Net
        '''
        if (_checkName(self.petriNet, newName)):
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
        if (guard is not None):
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
            if (_checkType(arc) != "InputArc"):
                raise Exception(
                    "Timed Transition's new Input Arc list's elements must be instances of class Input Arc")
            if (arc.petriNet != self.petriNet):
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
        if (_checkType(newInputArc) != "InputArc"):
            raise Exception(
                "Timed Transition's new Input Arc must be instance of class Input Arc")
        if (newInputArc.petriNet != self.petriNet):
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
            if (_checkType(arc) != "OutputArc"):
                raise Exception(
                    "Timed Transition's new Output Arc list's elements must be instances of class Output Arc")
            if (arc.petriNet != self.petriNet):
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
            if (arc.fromTrans is not None):
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
        if (_checkType(newOutputArc) != "OutputArc"):
            raise Exception(
                "Timed Transition's new Output Arc must be instance of class Output Arc")
        if (newOutputArc.petriNet != self.petriNet):
            raise Exception(
                "Timed Transition's new Output Arc must be assigned to same Petri Net of Timed Transition!")

        if (newOutputArc.fromTrans is not None):
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
            if (_checkType(arc) != "InhibArc"):
                raise Exception(
                    "Timed Transition's new Inhibitor Arc list's elements must be instances of class Inhibitor Arc")
            if (arc.petriNet != self.petriNet):
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
            if (arc.target is not None):
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
        if (_checkType(newInhibArc) != "InhibArc"):
            raise Exception(
                "Timed Transition's new Inhibitor Arc must be instance of class Inhibitor Arc")
        if (newInhibArc.petriNet != self.petriNet):
            raise Exception(
                "Timed Transition's new Inhibitor Arc must be assigned to same Petri Net of Timed Transition!")

        if (newInhibArc.target is not None):
            newInhibArc.target.inhibArcs.remove(newInhibArc)
        newInhibArc.target = self
        self.inhibArcs.append(newInhibArc)


def _checkName(petriNet, name):
    '''
    Helper method used to check if Timed Transition with given name already exists in given Petri Net.
    '''
    for trans in petriNet.timedTransList:
        if (trans.name == name):
            return False
    return True


def _checkType(object):
    '''
    Helper method used to return value type of given object.
    '''
    return object.__class__.__name__
