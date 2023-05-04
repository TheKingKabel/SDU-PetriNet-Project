# components/immediateTransitions.py module for Petri Net Project
# contains class definition for object type Immediate Transition

class ImmediateTransition:
    '''
    Class that represents an Immediate Transition object.
    '''

    def __init__(self, name: str, petriNet, guard=None, fireProbability: float = 1.0, fireCount: int = 0):
        '''
        Constructor method of the Immediate Transition class.
        Arguments:
            @param name: Name of the Immediate Transition, must be string, must be unique amongst Immediate Transition names in assigned Petri Net.
            @param petriNet: Reference of parent Petri Net object for Immediate Transition to be assigned to, must be instance of class PetriNet.
            @param guard (optional): Condition for Immediate Transition to be enabled for firing, must be reference to a callable function defined in the user file, returning boolean value True or False, i.e. "Queue.tokens >= 1". If not applicable, must be set to None. Default value: None.
            @param fireProbability (optional): Parameter used to calculate firing probability for competing Immediate Transitions, must be float, must be in between 0.0 (greater) and 1.0. Default value: 1.0 (100%).
            @param fireCount (optional): Parameter used to overwrite initial number of firings of Immediate Transition, used for statistics, must be integer, must not be smaller than 0. Default value: 0.
        '''

        # Type checks
        if(_checkType(petriNet) == "PetriNet"):
            # set reference of Petri Net to assign current Immediate Transition to
            self.petriNet = petriNet

            if (_checkName(petriNet, name)):
                # set name of the Immediate Transition
                self.name = str(name)

                # set guard function if correctly specified, set to None if not applicable
                if(guard is not None):
                    if(_checkType(guard()) == 'bool'):
                        # set guard function
                        self.guard = guard
                    else:
                        del self
                        raise Exception(
                            "The guard function added to Immediate Transition named: " + name + " is invalid")
                else:
                    # guard is not specified
                    self.guard = None

                # set probability of firing, default 1.0 (100%)
                # firing probability must be floating number between between 0.0 (greater than 0) and 1.0 (100%)
                if(_checkType(fireProbability) == 'float'):
                    if(fireProbability <= 0):
                        del self
                        raise Exception(
                            "The firing probability of Immediate Transition named: " + name + " must be greater than 0.0!")
                    elif(fireProbability > 1):
                        del self
                        raise Exception(
                            "The firing probability of Immediate Transition named: " + name + " must not be greater than 1.0!")
                    else:
                        self.fireProbability = fireProbability
                else:
                    del self
                    raise Exception(
                        "The firing probability value of Immediate Transition named: " + name + " must be a floating number!")

                # set number of times Immediate Transition has fired, default 0
                # fire count must be greater or equal than 0
                if(_checkType(fireCount) == 'int'):
                    if(fireCount < 0):
                        del self
                        raise Exception(
                            "The fireCount parameter of Immediate Transition named: " + name + " must not be smaller than 0!")
                    else:
                        self.fireCount = fireCount
                        self.initFireCount = fireCount
                else:
                    del self
                    raise Exception(
                        "The fireCount parameter of Immediate Transition named: " + name + " must be an integer number!")

                # set previous number of times Immediate Transition has fired, initially same value as fireCount (used for statistics)
                self.prevFireCount = fireCount

                # set if Immediate Transition is competing with other Immediate Transition, boolean, checked and set automatically at the start of simulation
                self.competing = False

                # set if Immediate Transition is enabled for firing, default: False, checked and set automatically during simulation
                self.enabled = False

                # list of Input Arcs targeting current Immediate Transition
                self.inputArcs = []

                # list of Output Arcs originating from current Immediate Transition
                self.outputArcs = []

                # list of Inhibitor Arcs targeting the current Immediate Transition
                self.inhibArcs = []

                # add Immediate Transition to PN's Immediate Transition list
                petriNet.immediateTransList.append(self)

            else:
                del self
                raise Exception(
                    "An Immediate Transition already exists named: " + name + ", in Petri Net named: " + petriNet.name)

        else:
            del self
            raise Exception(
                "Petri Net with name: " + petriNet + " does not exist!")

    def __str__(self):
        '''
        Returns user-friendly string representation (description) of Immediate Transition object.
        '''
        returnString = (
            f"Immediate Transition\n"
            f"\tname: {self.name},\n"
            f"\tin Petri Net named: {self.petriNet.name},\n"
            f"\twith guard function: {self.guard},\n"
            f"\tcurrently enabled: {self.enabled},\n"
            f"\tcompeting: {self.competing},\n"  # TODO: not set at this point?
            f"\twith firing possibility: {self.fireProbability},\n"
            f"\tcurrent firing times: {self.fireCount},\n"
            f"\tnumber of targeting Input Arcs: {len(self.inputArcs)},\n"
            "\tlist of targeting Input Arcs:\n")
        if(len(self.inputArcs) == 0):
            returnString += '\t\t' + 'None' + '\n'
        else:
            for arc in self.inputArcs:
                returnString += '\t\t' + \
                    '\t\t'.join(str(arc).splitlines(True)) + '\n'
        returnString += f"\tnumber of originating Output Arcs: {len(self.outputArcs)},\n"
        returnString += "\tlist of originating Output Arcs:\n"
        if(len(self.outputArcs) == 0):
            returnString += '\t\t' + 'None' + '\n'
        else:
            for arc in self.outputArcs:
                returnString += '\t\t' + \
                    '\t\t'.join(str(arc).splitlines(True)) + '\n'
        returnString += f"\tnumber of targeting Inhibitor Arcs: {len(self.inhibArcs)},\n"
        returnString += "\tlist of targeting Inhibitor Arcs:\n"
        if(len(self.inhibArcs) == 0):
            returnString += '\t\t' + 'None' + '\n'
        else:
            for arc in self.inhibArcs:
                returnString += '\t\t' + \
                    '\t\t'.join(str(arc).splitlines(True)) + '\n'

        return returnString

    def resetState(self):
        '''
        Resets the Immediate Transition to its initial state after a simulation run.
        '''
        self.fireCount = self.initFireCount
        self.prevFireCount = self.initFireCount
        self.competing = False
        self.enabled = False

    # TODO: delete getter setters, not needed?
    #
    #
    #

    # NAME

    def setName(self, newName: str):
        '''
        Setter function for name of Immediate Transition.
        @param newName: New name for Immediate Transition, must be string, must be unique in assigned Petri Net
        '''
        if (_checkName(self.petriNet, newName)):
            self.name = newName
        else:
            raise Exception(
                "An Immediate Transition already exists named: " + newName + ", in Petri Net named: " + self.petriNet.name)

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
        @param guard: New guard condition for Immediate Transition to enable firing, must be assessable logic statement in string, i.e. "Queue.tokens >= 1" TODO: please only use references to elements created in the SAME Petri Net class
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
            self.guard = None

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
        @param *inputArcList: New tuple of Input Arcs to be added to Immediate Transition's Input Arc list, must be a tuple of instances of class Input Arc, Input Arcs must be assigned to same Petri Net instance
        '''
        for arc in inputArcList:
            if(_checkType(arc) != "InputArc"):
                raise Exception(
                    "Immediate Transition's new Input Arc list's elements must be instances of class Input Arc")
            if(arc.petriNet != self.petriNet):
                raise Exception(
                    "Immediate Transition's new Input Arc list's elements must be assigned to same Petri Net of Immediate Transition!")

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
        Getter function for list of Input Arcs targeting current Immediate Transition.
        Returns current list of Input Arcs targeting current Immediate Transition.
        '''
        return self.inputArcs

    def addInputArc(self, newInputArc):
        '''
        Setter function to add new Input Arc targeting current Immediate Transition, to Immediate Transition's Input Arc list.
        Note: this function adds one new Input Arc to the Immediate Transition's Input Arc list. To overwrite the list with a tuple of multiple Input Arcs, use setInputArcs.
        @param newInputArc: New Input Arc to be added to Immediate Transition's Input Arc list, must be instance of class Input Arc, must be assigned to same Petri Net instance
        '''
        if(_checkType(newInputArc) != "InputArc"):
            raise Exception(
                "Immediate Transition's new Input Arc must be instance of class Input Arc")
        if(newInputArc.petriNet != self.petriNet):
            raise Exception(
                "Immediate Transition's new Input Arc must be assigned to same Petri Net of Immediate Transition!")

        if (newInputArc.toTrans is not None):
            newInputArc.toTrans.inputArcs.remove(newInputArc)
        newInputArc.toTrans = self
        self.inputArcs.append(newInputArc)

    # OUTPUT ARCS
    def setOutputArcs(self, *outputArcList):
        '''
        Setter function to overwrite Output Arcs originating from current Immediate Transition.
        Note: this function deletes existing list of Output Arcs, and creates new list with the given parameters. To add single new Output Arc to Immediate Transition's Output Arc list, use addOutputArc.
        @param *outputArcList: New tuple of Output Arcs to be added to Immediate Transition's Output Arc list, must be a tuple of instances of class Output Arc, Output Arcs must be assigned to same Petri Net instance
        '''
        for arc in outputArcList:
            if(_checkType(arc) != "OutputArc"):
                raise Exception(
                    "Immediate Transition's new Output Arc list's elements must be instances of class Output Arc")
            if(arc.petriNet != self.petriNet):
                raise Exception(
                    "Immediate Transition's new Output Arc list's elements must be assigned to same Petri Net of Immediate Transition!")

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
        Getter function for list of Output Arcs originating from current Immediate Transition.
        Returns current list of Output Arcs originating from current Immediate Transition.
        '''
        return self.outputArcs

    def addOutputArc(self, newOutputArc):
        '''
        Setter function to add new Output Arc originating from current Immediate Transition, to Immediate Transition's Output Arc list.
        Note: this function adds one new Output Arc to the Immediate Transition's Output Arc list. To overwrite the list with a tuple of multiple Output Arcs, use setOutputArcs.
        @param newOutputArc: New Output Arc to be added to Immediate Transition's Output Arc list, must be instance of class Output Arc, must be assigned to same Petri Net instance
        '''
        if(_checkType(newOutputArc) != "OutputArc"):
            raise Exception(
                "Immediate Transition's new Output Arc must be instance of class Output Arc")
        if(newOutputArc.petriNet != self.petriNet):
            raise Exception(
                "Immediate Transition's new Output Arc must be assigned to same Petri Net of Immediate Transition!")

        if(newOutputArc.fromTrans is not None):
            newOutputArc.fromTrans.outputArcs.remove(newOutputArc)
        newOutputArc.fromTrans = self
        self.outputArcs.append(newOutputArc)

    # INHIB ARCS
    def setInhibArcs(self, *inhibArcList):
        '''
        Setter function to overwrite Inhibitor Arcs targeting current Immediate Transition.
        Note: this function deletes existing list of Inhibitor Arcs, and creates new list with the given parameters. To add single new Inhibitor Arc to Immediate Transition's Inhibitor Arc list, use addInhibArc.
        @param *inhibArcList: New tuple of Inhibitor Arcs to be added to Immediate Transition's Inhibitor Arc list, must be a tuple of instances of class Inhibitor Arc, Inhibitor Arcs must be assigned to same Petri Net instance
        '''
        for arc in inhibArcList:
            if(_checkType(arc) != "InhibArc"):
                raise Exception(
                    "Immediate Transition's new Inhibitor Arc list's elements must be instances of class Inhibitor Arc")
            if(arc.petriNet != self.petriNet):
                raise Exception(
                    "Immediate Transition's new Inhibitor Arc list's elements must be assigned to same Petri Net of Immediate Transition!")

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
        Getter function for list of Inhibitor Arcs targeting current Immediate Transition.
        Returns current list of Inhibitor Arcs targeting current Immediate Transition.
        '''
        return self.inhibArcs

    def addInhibArc(self, newInhibArc):
        '''
        Setter function to add new Inhibitor Arc targeting current Immediate Transition, to Immediate Transition's Inhibitor Arc list.
        Note: this function adds one new Inhibitor Arc to the Immediate Transition's Inhibitor Arc list. To overwrite the list with a tuple of multiple Inhibitor Arcs, use setInhibArcs.
        @param newInhibArc: New Inhibitor Arc to be added to Immediate Transition's Inhibitor Arc list, must be instance of class Inhibitor Arc, must be assigned to same Petri Net instance
        '''
        if(_checkType(newInhibArc) != "InhibArc"):
            raise Exception(
                "Immediate Transition's new Inhibitor Arc must be instance of class Inhibitor Arc")
        if(newInhibArc.petriNet != self.petriNet):
            raise Exception(
                "Immediate Transition's new Inhibitor Arc must be assigned to same Petri Net of Immediate Transition!")

        if(newInhibArc.target is not None):
            newInhibArc.target.inhibArcs.remove(newInhibArc)
        newInhibArc.target = self
        self.inhibArcs.append(newInhibArc)


def _checkName(petriNet, name):
    for trans in petriNet.immediateTransList:
        if (trans.name == name):
            return False
    return True


def _checkType(object):
    return object.__class__.__name__
