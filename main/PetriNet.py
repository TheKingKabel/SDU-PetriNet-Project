# main/PetriNet.py module for Petri Net Project
# contains class definition for object type Petri Net
# TODO: to be imported to users' project modules

from components.immediateTransition import ImmediateTransition
from components.timedTransition import TimedTransition
from components.place import Place
from components.inputArc import InputArc
from components.outputArc import OutputArc
from components.inhibArc import InhibArc
from .simulation import simulation

# list of user created Petri Net's (in active module)
petriNetList = []


class PetriNet:
    '''
    Class that represents a Petri Net object.
    '''

    def __init__(self, name: str):
        '''
        Constructor method of the Petri Net class.
        Arguments:
            @param name: Name of the Petri Net, must be string, must be unique amongst Petri Net names created by user in the same module.
        '''

        # set name of the Petri Net
        self.name = str(name)

        # create lists to store different objects assigned to current Petri Net
        # list of Place assigned to current Petri Net
        self.placeList = []

        # list of Timed Transitions assigned to current Petri Net
        self.timedTransList = []

        # list of Immediate Transitions assigned to current Petri Net
        self.immediateTransList = []

        # list of Input Arcs assigned to current Petri Net
        self.inputArcList = []

        # list of Output Arcs assigned to current Petri Net
        self.outputArcList = []

        # list of Inhibitor Arcs assigned to current Petri Net
        self.inhibList = []

        # add Petri Net to list of Petri Nets created by user in current module
        petriNetList.append(self)

    def describe(self):
        '''
        Returns user-friendly textual description of the Petri Net object.
        '''
        print("Places:")
        print('\t'.join(self.getPlaces().splitlines(True)))
        print("Timed Transitions:")
        print('\t'.join(self.getTimedTransitions().splitlines(True)))
        print("Immediate Transitions:")
        print('\t'.join(self.getImmediateTransitions().splitlines(True)))
        print("Input Arcs:")
        print('\t'.join(self.getInputArcs().splitlines(True)))
        print("Output Arcs:")
        print('\t'.join(self.getOutputArcs().splitlines(True)))
        print("Inhibitor Arcs:")
        print('\t'.join(self.getInhibArcs().splitlines(True)))

    def getPlaces(self):
        '''
        Returns user-friendly string representation (description) of the Places assigned to the Petri Net object.
        '''
        returnString = ''
        if(len(self.placeList) == 0):
            return '\tNone\n'
        for place in self.placeList:
            returnString += '\n' + str(place)
        return returnString

    def getTimedTransitions(self):
        '''
        Returns user-friendly string representation (description) of the Timed Transitions assigned to the Petri Net object.
        '''
        returnString = ''
        if(len(self.timedTransList) == 0):
            return '\tNone\n'
        for timedTrans in self.timedTransList:
            returnString += '\n' + str(timedTrans)
        return returnString

    def getImmediateTransitions(self):
        '''
        Returns user-friendly string representation (description) of the Immediate Transitions assigned to the Petri Net object.
        '''
        returnString = ''
        if(len(self.immediateTransList) == 0):
            return '\tNone\n'
        for immediateTrans in self.immediateTransList:
            returnString += '\n' + str(immediateTrans)
        return returnString

    def getInputArcs(self):
        '''
        Returns user-friendly string representation (description) of the Input Arcs assigned to the Petri Net object.
        '''
        returnString = ''
        if(len(self.inputArcList) == 0):
            return '\tNone\n'
        for inputArc in self.inputArcList:
            returnString += '\n' + str(inputArc)
        return returnString

    def getOutputArcs(self):
        '''
        Returns user-friendly string representation (description) of the Output Arcs assigned to the Petri Net object.
        '''
        returnString = ''
        if(len(self.outputArcList) == 0):
            return '\tNone\n'
        for outputArc in self.outputArcList:
            returnString += '\n' + str(outputArc)
        return returnString

    def getInhibArcs(self):
        '''
        Returns user-friendly string representation (description) of the Inhibitor Arcs assigned to the Petri Net object.
        '''
        returnString = ''
        if(len(self.inhibList) == 0):
            return '\tNone\n'
        for inhibArc in self.inhibList:
            returnString += '\n' + str(inhibArc)
        return returnString

    def runSimulation(self, simLength: float, randomSeed: int = 1337, verbose: int = 1,  defTimeUnit: str = 'sec', conditionals=None, logPath: str = './logs'):
        # TODO: randomSeed, verbose ?
        '''
        Method to run a simulation on the Petri Net.
        Arguments:
            @param simLength: Time length of the simulation. Must be float, must not be smaller than 0.
            @param randomSeed:
            @param defTimeUnit (optional): Default time unit used in the simulation and result logs, must be chosen from predefined list. Generated Timed Transition delays with different assigned time units will be multiplied accordingly to match the default simulation time unit. Default value: 'sec' (seconds).
            @param conditionals: Specific states of the Petri Net where additional statistics is to be collected. Must be a list of tuples, each containing a string name of the conditions (for logging) and references to a callable functions defined in the user file, returning boolean value True or False, i.e. "Server.tokens >= 1". If not applicable, must be set to None. Default value: None.
            @param logPath (optional): Path of the folder where the simulation result logs will be generated in. Default value: root/logs/.
        '''
        simulation(self, simLength, randomSeed, verbose,
                   defTimeUnit, conditionals, logPath)
