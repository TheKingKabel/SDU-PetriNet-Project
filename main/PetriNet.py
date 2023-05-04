# main/PetriNet.py module for Petri Net Project
# contains class definition for object type Petri Net
# TODO: to be imported to users' project modules

import random
import os
from components.immediateTransition import ImmediateTransition
from components.timedTransition import TimedTransition
from components.place import Place
from components.inputArc import InputArc
from components.outputArc import OutputArc
from components.inhibArc import InhibArc
from definitions.timeunit_types import TimeUnitType
from .simulation import simulation
from .generateLogs import generatePNDescription, generatePNML, generateLogFile
from datetime import datetime

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

    def runSimulations(self, expLength: int, simLength: float, verbose: int = 1, randomSeed=None, defTimeUnit: str = 'sec', conditionals=None, logPath: str = './logs'):
        # TODO: verbose ?
        '''
        Method to run a simulation on the Petri Net.
        Arguments:
            @param expLength (required): Number of repetitions for the experiment to run individual simulations. Must be integer, must be greater than 0.
            @param simLength (required): Time length of simulations. Must be float, must not be smaller than 0.
            @param verbose (optional): Verbosity of log displayed in terminal (all results are generated into files regardless). Must be integer, must be greater or equal than 0. If set to 0: low verbosity, if higher than 0: high verbosity. Default value: 1.
            @param randomSeed (optional): Seed for the experiment to generate seeds for random choices and delay generations for individual simulation runs. Must be integer number between 0 and 2**32 - 1. Default value: randomly generated 32 bit sized integer value.
            @param defTimeUnit (optional): Default time unit used in the simulations and result logs, must be chosen from predefined list. Generated Timed Transition delays with different assigned time units will be multiplied accordingly to match the default simulation time unit. Default value: 'sec' (seconds).
            @param conditionals (optional): Specific states of the Petri Net where additional statistics is to be collected. Must be a list of tuples, each containing a string name of the conditions (for logging) and references to callable functions defined in the user file, returning boolean value True or False, i.e. "Server.tokens >= 1". If not applicable, must be set to None. Default value: None.
            @param logPath (optional): Path of the folder where the experiment result logs will be generated in (creates logs folder at destination). Default value: project root/logs/.
        '''

        # Type checking
        # experiment length
        if(not expLength.__class__.__name__ == 'int'):
            raise Exception(
                "The value: " + expLength + ", given as experiment length must be an integer.")
        elif(expLength <= 0):
            raise Exception(
                "The value: " + expLength + ", given as experiment length must be greater than 0.")

        # simulation length
        if(not(simLength.__class__.__name__ == 'int' or simLength.__class__.__name__ == 'float')):
            raise Exception(
                "The value: " + simLength + ", given as time length of simulations must be an integer or float number.")
        elif(simLength <= 0):
            raise Exception(
                "The value: " + simLength + ", given as time length of simulations must be greater than 0.")

        # verbose
        # TODO: add multiple verbose options?
        if(not (verbose == 0 or verbose == 1)):
            raise Exception(
                "The value: " + verbose + ", given as verbosity setting is not 0 or 1.")

        # random experiment seed
        # list of simulation seeds for replicability
        expSeeds = []

        # set seed for generation of simulation seeds
        if(randomSeed is not None):
            if(not randomSeed.__class__.__name__ == 'int'):
                raise Exception(
                    "The value: " + randomSeed + ", given as random seed for experiment must be an integer.")
            elif(randomSeed < 0 or randomSeed > (2**32 - 1)):
                raise Exception(
                    "The value: " + randomSeed + ", given as random seed for experiment must be between 0 and 2**32 - 1 (4294967295)")
            try:
                random.seed(randomSeed)
            except:
                raise Exception(
                    "The value: " + randomSeed + ", given as random seed is invalid.")
        else:
            # numpy accepts 32 bit sized integer values for seed
            randomSeed = random.randrange(2**32)
            random.seed(randomSeed)

        # default time unit setting of simulations
        timeTypes = [member.name for member in TimeUnitType]

        if(defTimeUnit not in timeTypes):
            returnMsg = "The default time unit type set for simulation of Petri Net named: " + \
                PetriNet.name + " is not defined.\nSupported time unit types: "
            for member in TimeUnitType:
                returnMsg += '[' + member.name + \
                    ": " + member.value + '], '
            raise Exception(
                returnMsg)

        # conditionals
        if(conditionals is not None):
            for condition in conditionals:
                cond_error = False
                wrong_func = -1
                for func_nbr in range(0, len(condition)-1):
                    if(not condition[func_nbr+1]().__class__.__name__ == 'bool'):
                        cond_error = True
                        wrong_func = func_nbr+1
                        break
                if(cond_error):
                    returnMsg = "The function reference: " + \
                        str(condition[wrong_func].__name__) + \
                        ', in conditional: ' + \
                        '(\'' + str(condition[0]) + '\', '
                    for func_nbr in range(0, len(condition)-1):
                        returnMsg += str(condition[func_nbr+1].__name__)
                        if(not func_nbr+1 == (len(condition)-1)):
                            returnMsg += ', '
                    returnMsg += ') does not return boolean value.'
                    raise Exception(returnMsg)

        # logPath
        if(not logPath == './logs'):
            logPath = logPath + '/logs'
            if (not os.path.exists(os.path.dirname(logPath))):
                try:
                    os.makedirs(os.path.dirname(logPath))
                except:
                    raise Exception(
                        "The given path: " + logPath + " is invalid, couldn\'t create logs folder.")

        # generate .txt description and .pnml file from model
        PNDescFileName = logPath + '/' + self.name + '/' + self.name + '_PetriNet.txt'
        generatePNDescription(self, PNDescFileName)
        # TODO:
        pnmlFileName = logPath + '/' + self.name + '/' + self.name + '_PetriNet.pnml'
        generatePNML(self, pnmlFileName)

        # save the starting timestamp of experiment
        exp_start = datetime.now()

        # filename and logpath to create experiment logs
        experimentFolderPath = logPath + '/' + self.name + '/Experiment_' + \
            exp_start.strftime("%Y-%m-%d-%H-%M-%S-%f") + '/'
        experimentFileName = experimentFolderPath + \
            self.name + '_Experiment_Results.txt'

        # create and start logging experiment
        generateLogFile(str(self.name) + " Petri Net experiment, seed: " +
                        str(randomSeed) + "\n\nSimulations' seeds (" + str(expLength) + "):", experimentFileName, verbose)
        for i in range(expLength):
            seed = random.randrange(2**32)
            expSeeds.append(seed)
            generateLogFile(
                "\t" + str(i+1) + ". sim. seed.: " + str(seed), experimentFileName, verbose)

        generateLogFile("\nExperiment started at: " +
                        str(exp_start) + "\n", experimentFileName, verbose)
        # logpath to create single simulation logs
        simulationsFolderPath = experimentFolderPath + 'Simulation_results' + '/'

        # store final marking and statistics of each simulation run
        finalMarking = []
        finalMarkingCount = []
        finalMarkingTotalTime = []
        finalMarkingTimeRatio = []

        # store the results for conditionals of each simulation run
        conditionalCount = []
        conditionalRatio = []
        conditionalTotalTime = []
        conditionalTimeRatio = []

        # run simulations according to experiment length
        for experiment in range(expLength):

            # record timestamp of simulation run start (for statistics)
            start = datetime.now()

            generateLogFile('\t' + str(experiment+1) + ". simulation run, seed: " + str(expSeeds[experiment]) + ", started at: " +
                            str(start), experimentFileName, verbose)

            # filename to create single simulation log
            simulationFolderName = simulationsFolderPath + \
                'Sim_Run' + str(experiment+1) + '/'

            # run individual simulation with given parameters, save results
            simMark, simMarkCount, simMarkTotalTime, simMarkTimeRatio, simCondCounts, simCondRatios, simCondTotalTimes, simCondTimeRatios = simulation(
                self, simLength, expSeeds[experiment], verbose, defTimeUnit, conditionals, simulationFolderName, experiment+1)

            # print final marking results
            generateLogFile("\n\tSimulation run final marking:\n\t\tMarking, nbr. of occurrence, total time spent in marking, ratio of time spent in marking:\n\t\t\t" +
                            str(simMark) + ': ' + str(simMarkCount) + ', ' + str(simMarkTotalTime) +
                            ' ' + defTimeUnit + ', ' + str(simMarkTimeRatio), experimentFileName, verbose)

            # print simulation conditionals results
            logText = "\n\tSimulation run conditionals:\n\t\tAdditional conditions, nbr. of occurrence, ratio of occurrence / nbr. of states, total time spent while true, ratio of time spent while true:\n"
            if(conditionals is None):
                logText += "\t\t\tNone\n"
            else:
                for id, cond in enumerate(conditionals):
                    logText += '\t\t\t' + str(cond[0]) + ': ' + str(simCondCounts[id]) + ', ' + str(
                        simCondRatios[id]) + ', ' + str(simCondTotalTimes[id]) + ' ' + defTimeUnit + ', ' + str(simCondTimeRatios[id]) + '\n'

            generateLogFile(logText, experimentFileName, verbose)

            # append results to their appropriate list
            conditionalCount.append(simCondCounts)
            conditionalRatio.append(simCondRatios)
            conditionalTotalTime.append(simCondTotalTimes)
            conditionalTimeRatio.append(simCondTimeRatios)

            # record timestamp of simulation run end (for statistics)
            end = datetime.now()

            # write results of simulation run to experiment log
            generateLogFile(
                "\n\tSimulation run finished at: " + str(datetime.now()) + "\n\tElapsed time: " + str(end - start) + "\n", experimentFileName, verbose)

            # reset the Petri Net to its initial state
            for immediateTrans in self.immediateTransList:
                immediateTrans.resetState()
            for timedTrans in self.timedTransList:
                timedTrans.resetState()
            for place in self.placeList:
                place.resetState()

        # save the ending timestamp of experiment
        exp_end = datetime.now()

        generateLogFile("Experiment ended at: " + str(exp_end) + "\nElapsed time: " +
                        str(exp_end-exp_start) + "\n", experimentFileName, verbose)
