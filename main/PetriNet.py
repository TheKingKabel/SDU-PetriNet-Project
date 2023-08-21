# main/PetriNet.py module for Petri Net Project
# contains class definition for object type Petri Net
# TODO: to be imported to users' project modules


import random
import statistics
import math
import os
import scipy
import xml.etree.ElementTree as ET
from components.immediateTransition import ImmediateTransition
from components.timedTransition import TimedTransition
from components.place import Place
from components.inputArc import InputArc
from components.outputArc import OutputArc
from components.inhibArc import InhibArc
from definitions.timeunit_types import TimeUnitType
from .simulation import simulation
from .generateLogs import generatePNDescription, generatePNML, generateLogFile, generatePNGraph
from datetime import datetime


# list of user created Petri Net's (in active module)
petriNetList = []


def createNewPN(name: str):
    '''
    Method used to create (define) new instance of Petri Net class.
    Calls the default constructor method (init) with same parameters.
    Arguments:
        @param name: Name of the Petri Net, must be string, must be unique amongst Petri Net names created by user in the same module.
    '''
    return PetriNet(name)


def loadExistingPN(filePath: str, newName: str = None):
    '''
    Method used to load pre-defined Petri Net from the given (generated) .pnml file.
    Arguments:
        @param filePath: Path of the generated .pnml file to generate Petri Net object from.
        @param newName (optional): New name for the reconstructed Petri Net (will not overwrite already existing Petri Net files with old name).
    '''

    # check if file exists at path
    if (not os.path.isfile(filePath)):
        raise Exception("The file in: " + str(filePath) + " does not exist.")

    # check if file extension is .pnml
    if (not filePath.endswith('.pnml')):
        raise Exception("The file in: " + str(filePath) +
                        " is not a .pnml file.")

    # using XML parser to read .pnml file
    namespace = {'pnml': 'http://www.pnml.org/version-2009/grammar/pnml'}
    tree = ET.parse(filePath)
    root = tree.getroot()

    # create Petri Net dictionary to identify and store references to nodes by id
    PNDict = {}

    # create Petri Net object
    if (newName is None):
        PN_name = root.find('.//pnml:page/pnml:name/pnml:text', namespace).text
    else:
        PN_name = str(newName)
    petriNet = PetriNet(PN_name)

    # PLACES
    PNDict.update({"places": {}})
    for element in root.findall('.//pnml:place', namespace):

        place_name = element.find('pnml:name/pnml:text', namespace).text
        place_initT = element.find(
            'pnml:initialMarking/pnml:text', namespace).text
        place_initTT = element.find(
            'pnml:initialTotalTokens/pnml:text', namespace).text
        place_initMT = element.find(
            'pnml:initialMaxTokens/pnml:text', namespace).text

        # create Place object
        place = Place(str(place_name), petriNet, int(place_initT),
                      int(place_initTT), int(place_initMT))

        # store place reference in dictionary
        PNDict["places"].update({element.get('id'): place})

    # TRANSITIONS
    PNDict.update({"transitions": {}})

    # TIMED TRANSITIONS
    for element in root.findall('.//pnml:transition[@type="timed"]', namespace):

        transition_name = element.find('pnml:name/pnml:text', namespace).text
        transition_distType = element.find(
            'pnml:distributionType/pnml:text', namespace).text
        transition_distArg1 = element.find(
            'pnml:distributionArg1/pnml:text', namespace).text
        transition_distArg2 = element.find(
            'pnml:distributionArg2/pnml:text', namespace).text
        transition_distArg3 = element.find(
            'pnml:distributionArg3/pnml:text', namespace).text
        transition_distArg4 = element.find(
            'pnml:distributionArg4/pnml:text', namespace).text
        transition_timeUnit = element.find(
            'pnml:timeUnit/pnml:text', namespace).text
        transition_agePolicy = element.find(
            'pnml:agePolicy/pnml:text', namespace).text

        # create guard function dynamically
        if (element.find('pnml:guard/pnml:text', namespace).text == 'None'):
            transition_guard = None
        else:
            # exec() usage TODO: check documentation!
            exec(element.find('pnml:guard/pnml:code/pnml:text', namespace).text)
            transition_guard = globals()[element.find(
                'pnml:guard/pnml:name/pnml:text', namespace).text]

        transition_fireCount = element.find(
            'pnml:fireCount/pnml:text', namespace).text

        # create Timed Transition object
        timedTransition = TimedTransition(str(transition_name), petriNet, transition_distType, float(transition_distArg1), float(transition_distArg2),
                                          float(transition_distArg3), float(
                                              transition_distArg4), transition_timeUnit, transition_agePolicy,
                                          transition_guard, int(transition_fireCount))

        # store transition reference in dictionary
        PNDict["transitions"].update({element.get('id'): timedTransition})

    # IMMEDIATE TRANSITIONS
    for element in root.findall('.//pnml:transition[@type="immediate"]', namespace):

        transition_name = element.find('pnml:name/pnml:text', namespace).text

        # create guard function dynamically
        if (element.find('pnml:guard/pnml:text', namespace).text == 'None'):
            transition_guard = None
        else:
            exec(element.find('pnml:guard/pnml:code/pnml:text', namespace).text)
            transition_guard = globals()[element.find(
                'pnml:guard/pnml:name/pnml:text', namespace).text]

        transition_fireProbability = element.find(
            'pnml:fireProbability/pnml:text', namespace).text
        transition_fireCount = element.find(
            'pnml:fireCount/pnml:text', namespace).text

        # create Immediate Transition object
        immediateTransition = ImmediateTransition(
            str(transition_name), petriNet, transition_guard, float(transition_fireProbability), int(transition_fireCount))

        # store transition reference in dictionary
        PNDict["transitions"].update({element.get('id'): immediateTransition})

    # ARCS

    # INPUT ARCS
    for element in root.findall('.//pnml:arc[@type="input"]', namespace):

        arc_name = element.find('pnml:name/pnml:text', namespace).text

        # multiplicity is static (number)
        if ((element.find('pnml:inscription/pnml:text', namespace).text).isdigit()):
            arc_multiplicity = int(element.find(
                'pnml:inscription/pnml:text', namespace).text)
        else:
            # multiplicity is dynamic (function)
            exec(element.find('pnml:inscription/pnml:code/pnml:text', namespace).text)
            arc_multiplicity = globals()[element.find(
                'pnml:inscription/pnml:name/pnml:text', namespace).text]

        # get place/transition id to find reference from PN dictionary
        arc_source = element.get('source')
        arc_target = element.get('target')

        # create Input Arc object
        inputArc = InputArc(str(
            arc_name), petriNet, PNDict['places'][arc_source], PNDict['transitions'][arc_target], arc_multiplicity)

    # OUTPUT ARCS
    for element in root.findall('.//pnml:arc[@type="output"]', namespace):

        arc_name = element.find('pnml:name/pnml:text', namespace).text

        # multiplicity is static (number)
        if ((element.find('pnml:inscription/pnml:text', namespace).text).isdigit()):
            arc_multiplicity = int(element.find(
                'pnml:inscription/pnml:text', namespace).text)
        else:
            # multiplicity is dynamic (function)
            exec(element.find('pnml:inscription/pnml:code/pnml:text', namespace).text)
            arc_multiplicity = globals()[element.find(
                'pnml:inscription/pnml:name/pnml:text', namespace).text]

        # get place/transition id to find reference from PN dictionary
        arc_source = element.get('source')
        arc_target = element.get('target')

        # create Output Arc object
        outputArc = OutputArc(str(
            arc_name), petriNet, PNDict['transitions'][arc_source], PNDict['places'][arc_target], arc_multiplicity)

    # INHIBITOR ARCS
    for element in root.findall('.//pnml:arc[@type="inhibitor"]', namespace):

        arc_name = element.find('pnml:name/pnml:text', namespace).text

        # multiplicity is static (number)
        if ((element.find('pnml:inscription/pnml:text', namespace).text).isdigit()):
            arc_multiplicity = int(element.find(
                'pnml:inscription/pnml:text', namespace).text)
        else:
            # multiplicity is dynamic (function)
            exec(element.find('pnml:inscription/pnml:code/pnml:text', namespace).text)
            arc_multiplicity = globals()[element.find(
                'pnml:inscription/pnml:name/pnml:text', namespace).text]

        # get place/transition id to find reference from PN dictionary
        arc_source = element.get('source')
        arc_target = element.get('target')

        # create Inhibitor Arc object
        inhibitorArc = InhibArc(str(arc_name), petriNet,
                                PNDict['places'][arc_source], PNDict['transitions'][arc_target], arc_multiplicity)

    # return Petri Net object
    return petriNet


class PetriNet:
    '''
    Class that represents a Petri Net object.
    '''

    def __init__(self, name: str):
        '''
        (Default) Constructor method of the Petri Net class.
        Arguments:
            @param name: Name of the Petri Net, must be string, must be unique amongst Petri Net names created by user in the same module.
        '''

        if (_checkName(name)):
            # set name of the Petri Net
            self.name = str(name)
        else:
            del self
            raise Exception("A Petri Net named: " +
                            str(name) + " already exists")

        # create lists to store various PN objects assigned to current Petri Net
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
        if (len(self.placeList) == 0):
            return '\tNone\n'
        for place in self.placeList:
            returnString += '\n' + str(place)
        return returnString

    def findPlaceByName(self, placeName):
        '''
        Method to search for a specific Place object assigned to current Petri Net (names are unique). Returns reference to Place.
        '''
        for place in self.placeList:
            if (place.name == placeName):
                return place
        raise Exception('Place does not exists with name: ' + name)

    def getTimedTransitions(self):
        '''
        Returns user-friendly string representation (description) of the Timed Transitions assigned to the Petri Net object.
        '''
        returnString = ''
        if (len(self.timedTransList) == 0):
            return '\tNone\n'
        for timedTrans in self.timedTransList:
            returnString += '\n' + str(timedTrans)
        return returnString

    def findTimedTransitionByName(self, transName):
        '''
        Method to search for a specific Timed Transition object assigned to current Petri Net (names are unique). Returns reference to Timed Transition.
        '''
        for trans in self.timedTransList:
            if (trans.name == transName):
                return trans
        raise Exception('Timed Transition does not exists with name: ' + name)

    def getImmediateTransitions(self):
        '''
        Returns user-friendly string representation (description) of the Immediate Transitions assigned to the Petri Net object.
        '''
        returnString = ''
        if (len(self.immediateTransList) == 0):
            return '\tNone\n'
        for immediateTrans in self.immediateTransList:
            returnString += '\n' + str(immediateTrans)
        return returnString

    def findImmediateTransitionByName(self, transName):
        '''
        Method to search for a specific Immediate Transition object assigned to current Petri Net (names are unique). Returns reference to Immediate Transition.
        '''
        for trans in self.immediateTransList:
            if (trans.name == transName):
                return trans
        raise Exception(
            'Immediate Transition does not exists with name: ' + name)

    def getInputArcs(self):
        '''
        Returns user-friendly string representation (description) of the Input Arcs assigned to the Petri Net object.
        '''
        returnString = ''
        if (len(self.inputArcList) == 0):
            return '\tNone\n'
        for inputArc in self.inputArcList:
            returnString += '\n' + str(inputArc)
        return returnString

    def findInputArcByName(self, inputName):
        '''
        Method to search for a specific Input Arc object assigned to current Petri Net (names are unique). Returns reference to Input Arc.
        '''
        for inputArc in self.inputArcList:
            if (inputArc.name == name):
                return inputArc
        raise Exception('Input Arc does not exists with name: ' + name)

    def getOutputArcs(self):
        '''
        Returns user-friendly string representation (description) of the Output Arcs assigned to the Petri Net object.
        '''
        returnString = ''
        if (len(self.outputArcList) == 0):
            return '\tNone\n'
        for outputArc in self.outputArcList:
            returnString += '\n' + str(outputArc)
        return returnString

    def findOutputArcByName(self, outputName):
        '''
        Method to search for a specific Output Arc object assigned to current Petri Net (names are unique). Returns reference to Output Arc.
        '''
        for outputArc in self.outputArcList:
            if (outputArc.name == name):
                return outputArc
        raise Exception('Output Arc does not exists with name: ' + name)

    def getInhibArcs(self):
        '''
        Returns user-friendly string representation (description) of the Inhibitor Arcs assigned to the Petri Net object.
        '''
        returnString = ''
        if (len(self.inhibList) == 0):
            return '\tNone\n'
        for inhibArc in self.inhibList:
            returnString += '\n' + str(inhibArc)
        return returnString

    def findInhibArcByName(self, inhibName):
        '''
        Method to search for a specific Inhibitor Arc object assigned to current Petri Net (names are unique). Returns reference to Inhibitor Arc.
        '''
        for inhibArc in self.inhibList:
            if (inhibArc.name == inhibName):
                return inhibArc
        raise Exception('Inhibitor Arc does not exists with name: ' + name)

    def runSimulations(self, expLength: int, simLength: float, verbose: int = 2, randomSeed=None, defTimeUnit: str = 'sec', conditionals=None, logPath: str = './logs'):
        # TODO: verbose ?
        '''
        Method to run an experiment on the Petri Net.
        Arguments:
            @param expLength: Number of repetitions for the experiment to run individual simulations. Must be integer, must be greater than 0.
            @param simLength: Time length of simulations. Must be float, must not be smaller than 0.
            @param verbose (optional): Verbosity of log displayed in terminal and file generation. Must be integer, must be 0, 1 or 2. If set to 0: low verbosity, no log is generated to terminal, only PN .pnml, PN graph, PN description, experiment log, and simulation .csv files are generated. If set to 1: medium verbosity, no log is generated to terminal, all files are generated. If set to 2: high verbosity, all logs are generated to terminal, all files are generated. Default value: 2.
            @param randomSeed (optional): Seed for the experiment to generate seeds for random choices and delay generations for individual simulation runs. Must be integer number between 0 and 2**32 - 1. Default value: randomly generated 32 bit sized integer value.
            @param defTimeUnit (optional): Default time unit used in the simulations and result logs, must be chosen from predefined list. Generated Timed Transition delays with different assigned time units will be multiplied accordingly to match the default simulation time unit. Default value: 'sec' (seconds).
            @param conditionals (optional): Specific states of the Petri Net where additional statistics is to be collected. Must be a list of tuples, each containing a string name of the conditions (for logging) and references to callable functions defined in the user file, returning boolean value True or False, i.e. "PetriNet.findPlaceByName("Server").tokens >= 1". If not applicable, must be set to None. Default value: None.
            @param logPath (optional): Path of the folder where the experiment result logs will be generated in (creates logs folder at destination). Default value: project root/logs/.
        '''

        # Type checking

        # experiment length
        if (not expLength.__class__.__name__ == 'int'):
            raise Exception(
                "The value: " + expLength + ", given as experiment length must be an integer.")
        elif (expLength <= 0):
            raise Exception(
                "The value: " + expLength + ", given as experiment length must be greater than 0.")

        # simulation length
        if (not (simLength.__class__.__name__ == 'int' or simLength.__class__.__name__ == 'float')):
            raise Exception(
                "The value: " + simLength + ", given as time length of simulations must be an integer or float number.")
        elif (simLength <= 0):
            raise Exception(
                "The value: " + simLength + ", given as time length of simulations must be greater than 0.")

        # verbose
        # TODO: add multiple verbose options?
        if (not (verbose == 0 or verbose == 1 or verbose == 2)):
            raise Exception(
                "The value: " + verbose + ", given as verbosity setting is not 0, 1 or 2.")

        file_verbose = verbose
        if (verbose < 2):
            file_verbose = 1

        # random experiment seed
        # list of simulation seeds for replicability
        expSeeds = []

        # set seed for generation of simulation seeds
        if (randomSeed is not None):
            if (not randomSeed.__class__.__name__ == 'int'):
                raise Exception(
                    "The value: " + randomSeed + ", given as random seed for experiment must be an integer.")
            elif (randomSeed < 0 or randomSeed > (2**32 - 1)):
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

        if (defTimeUnit not in timeTypes):
            returnMsg = "The default time unit type set for simulation of Petri Net named: " + \
                PetriNet.name + " is not defined.\nSupported time unit types: "
            for member in TimeUnitType:
                returnMsg += '[' + member.name + \
                    ": " + member.value + '], '
            raise Exception(
                returnMsg)

        # conditionals
        if (conditionals is not None):
            for condition in conditionals:
                cond_error = False
                wrong_func = -1
                # check conditional description
                if (not condition[0].__class__.__name__ == 'str'):
                    returnMsg = "The conditional description: " + str(condition[0]) + ", for conditional: (\'" + str(condition[0]) + \
                        '\', alpha = ' + str(condition[1]) + ', '
                    for func_nbr in range(0, len(condition)-2):
                        returnMsg += str(condition[func_nbr+2].__name__)
                        if (not func_nbr+2 == (len(condition)-2)):
                            returnMsg += ', '
                    returnMsg += ') is not a string.'
                    raise Exception(returnMsg)
                # check conditional alpha value
                if (not (condition[1].__class__.__name__ == 'int' or condition[1].__class__.__name__ == 'float')):
                    returnMsg = "The conditional alpha value: " + str(condition[1]) + ", for conditional: (\'" + str(condition[0]) + \
                        '\', alpha = ' + str(condition[1]) + ', '
                    for func_nbr in range(0, len(condition)-2):
                        returnMsg += str(condition[func_nbr+2].__name__)
                        if (not func_nbr+2 == (len(condition)-2)):
                            returnMsg += ', '
                    returnMsg += ') is not a number.'
                    raise Exception(returnMsg)
                if (condition[1] < 0.0 or condition[1] >= 1.0):
                    returnMsg = "The conditional alpha value: " + str(condition[1]) + ", for conditional: (\'" + str(condition[0]) + \
                        '\', alpha = ' + str(condition[1]) + ', '
                    for func_nbr in range(0, len(condition)-2):
                        returnMsg += str(condition[func_nbr+2].__name__)
                        if (not func_nbr+2 == (len(condition)-2)):
                            returnMsg += ', '
                    returnMsg += ') must be greater than 0, but smaller than 1.0 (100%).'
                    raise Exception(returnMsg)
                for func_nbr in range(0, len(condition)-2):
                    if (not condition[func_nbr+2]().__class__.__name__ == 'bool'):
                        cond_error = True
                        wrong_func = func_nbr+2
                        break
                if (cond_error):
                    returnMsg = "The function reference: " + \
                        str(condition[wrong_func].__name__) + \
                        ', in conditional: ' + \
                        '(\'' + str(condition[0]) + \
                        '\', alpha = ' + str(condition[1]) + ', '
                    for func_nbr in range(0, len(condition)-2):
                        returnMsg += str(condition[func_nbr+2].__name__)
                        if (not func_nbr+2 == (len(condition)-2)):
                            returnMsg += ', '
                    returnMsg += ') does not return boolean value.'
                    raise Exception(returnMsg)

        # logPath
        if (not logPath == './logs'):
            logPath = logPath + '/logs'
            if (not os.path.exists(os.path.dirname(logPath))):
                try:
                    os.makedirs(os.path.dirname(logPath))
                except:
                    raise Exception(
                        "The given path: " + logPath + " is invalid, couldn\'t create logs folder.")

        # generate .txt description and .pnml file from model
        # TXT description
        PNDescFileName = logPath + '/' + self.name + '/' + self.name + '_PetriNet.txt'
        generatePNDescription(self, PNDescFileName)
        # PNML file
        pnmlFileName = logPath + '/' + self.name + '/' + self.name + '_PetriNet.pnml'
        generatePNML(self, pnmlFileName)
        # PN graph
        PNGraphFile = logPath + '/' + self.name + '/'
        generatePNGraph(self, PNGraphFile)

        # save the starting timestamp of experiment
        exp_start = datetime.now()

        # filename and logpath to create experiment logs
        experimentFolderPath = logPath + '/' + self.name + '/Experiment_' + \
            exp_start.strftime("%Y-%m-%d-%H-%M-%S-%f") + '/'
        experimentFileName = experimentFolderPath + \
            self.name + '_Experiment_Results.txt'

        # create and start logging experiment
        generateLogFile(str(self.name) + " Petri Net experiment, seed: " +
                        str(randomSeed) + "\n\nSimulations' seeds (" + str(expLength) + "):", experimentFileName, file_verbose)
        for i in range(expLength):
            seed = random.randrange(2**32)
            expSeeds.append(seed)
            generateLogFile(
                "\t" + str(i+1) + ". sim. seed.: " + str(seed), experimentFileName, file_verbose)

        generateLogFile("\nExperiment started at: " +
                        str(exp_start) + "\n", experimentFileName, file_verbose)

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

        if (conditionals is not None):
            for condition in conditionals:
                conditionalCount.append([])
                conditionalRatio.append([])
                conditionalTotalTime.append([])
                conditionalTimeRatio.append([])

        # run simulations according to experiment length
        for experiment in range(expLength):

            # record timestamp of simulation run start (for statistics)
            start = datetime.now()

            generateLogFile('\t' + str(experiment+1) + ". simulation run, seed: " + str(expSeeds[experiment]) + ", started at: " +
                            str(start), experimentFileName, file_verbose)

            # filename to create single simulation log
            simulationFolderName = simulationsFolderPath + \
                'Sim_Run' + str(experiment+1) + '/'

            # run individual simulation with given parameters, save results
            simMark, simMarkCount, simMarkTotalTime, simMarkTimeRatio, simCondCounts, simCondRatios, simCondTotalTimes, simCondTimeRatios = simulation(
                self, simLength, expSeeds[experiment], verbose, defTimeUnit, conditionals, simulationFolderName, experiment+1)

            # print final marking results
            generateLogFile("\n\tSimulation run final marking:\n\t\tMarking, nbr. of occurrence, total time spent in marking, ratio of time spent in marking:\n\t\t\t" +
                            str(simMark) + ': ' + str(simMarkCount) + ', ' + str(simMarkTotalTime) +
                            ' ' + defTimeUnit + ', ' + str(simMarkTimeRatio), experimentFileName, file_verbose)

            # print simulation conditionals results
            logText = "\n\tSimulation run conditionals:\n\t\tAdditional conditions, nbr. of occurrence, ratio of occurrence / nbr. of states, total time spent while true, ratio of time spent while true:\n"

            # append marking results to their appropriate list
            finalMarking.append(simMark)
            finalMarkingCount.append(simMarkCount)
            finalMarkingTotalTime.append(simMarkTotalTime)
            finalMarkingTimeRatio.append(simMarkTimeRatio)

            if (conditionals is None):
                logText += "\t\t\tNone\n"
            else:
                for id, cond in enumerate(conditionals):
                    logText += '\t\t\t' + str(cond[0]) + ': ' + str(simCondCounts[id]) + ', ' + str(
                        simCondRatios[id]) + ', ' + str(simCondTotalTimes[id]) + ' ' + defTimeUnit + ', ' + str(simCondTimeRatios[id]) + '\n'

                    # append conditional results to their appropriate list
                    conditionalCount[id].append(simCondCounts[id])
                    conditionalRatio[id].append(simCondRatios[id])
                    conditionalTotalTime[id].append(simCondTotalTimes[id])
                    conditionalTimeRatio[id].append(simCondTimeRatios[id])

            generateLogFile(logText, experimentFileName, file_verbose)

            # record timestamp of simulation run end (for statistics)
            end = datetime.now()

            # write results of simulation run to experiment log
            generateLogFile(
                "\n\tSimulation run finished at: " + str(datetime.now()) + "\n\tElapsed time: " + str(end - start) + "\n", experimentFileName, file_verbose)

            # reset the Petri Net to its initial state
            for immediateTrans in self.immediateTransList:
                immediateTrans._resetState()
            for timedTrans in self.timedTransList:
                timedTrans._resetState()
            for place in self.placeList:
                place._resetState()

        # calculate confidence intervals for conditional results

        logText = "Conditionals' confidence interval results:\n\tConditional, T-value (alpha value%),\n\t\tmean of nbr. of occurrences, standard deviation of nbr. of occurrences, confidence interval for nbr. of occurrences,\n\t\tmean of ratio of occurrence / nbr. of states, standard deviation of ratio of occurrence / nbr. of states, confidence interval for ratio of occurrence / nbr. of states,\n\t\tmean of total time spent while true, standard deviation of total time spent while true, confidence interval for total time spent while true,\n\t\tmean of ratio of time spent while true, standard deviation of ratio of time spent while true, confidence interval for ratio of time spent while true\n"
        if (conditionals is not None):
            for id, condition in enumerate(conditionals):

                t_val = scipy.stats.t.ppf(q=1-condition[1], df=expLength)

                logText += "\n\t" + \
                    str(condition[0]) + ": " + str(t_val) + \
                    ' (' + str(condition[1]*100) + ' %)'

                # nbr. of occurrences
                avg = statistics.mean(conditionalCount[id])
                std = statistics.stdev(conditionalCount[id])
                logText += "\n\t\t" + str(avg) + ', ' + str(std) + ', CI = ' + str(
                    avg) + ' +/- ' + str(t_val * (std/math.sqrt(expLength)))

                # ratio of occurrence / nbr. of states
                avg = statistics.mean(conditionalRatio[id])
                std = statistics.stdev(conditionalRatio[id])
                logText += '\n\t\t' + str(avg) + ', ' + str(std) + ', CI = ' + str(
                    avg) + ' +/- ' + str(t_val * (std/math.sqrt(expLength)))

                # total time spent while true
                avg = statistics.mean(conditionalTotalTime[id])
                std = statistics.stdev(conditionalTotalTime[id])
                logText += '\n\t\t' + str(avg) + ', ' + str(std) + ', CI = ' + str(
                    avg) + ' +/- ' + str(t_val * (std/math.sqrt(expLength)))

                # ratio of time spent while true
                avg = statistics.mean(conditionalTimeRatio[id])
                std = statistics.stdev(conditionalTimeRatio[id])
                logText += '\n\t\t' + str(avg) + ', ' + str(std) + ', CI = ' + str(
                    avg) + ' +/- ' + str(t_val * (std/math.sqrt(expLength))) + '\n'
        else:
            logText += "\n\tNone\n"

        generateLogFile(logText, experimentFileName, file_verbose)

        # save the ending timestamp of experiment
        exp_end = datetime.now()

        generateLogFile("Experiment ended at: " + str(exp_end) + "\nElapsed time: " +
                        str(exp_end-exp_start) + "\n", experimentFileName, file_verbose)


def _checkName(name: str):
    '''
    Helper method used to return value type of given object.
    '''
    for petriNet in petriNetList:
        if (petriNet.name == name):
            return False
    return True
