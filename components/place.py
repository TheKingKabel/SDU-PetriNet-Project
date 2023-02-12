from PetriNet import placeList


class Place:

    def __init__(self, name: str, tokens: int = 0, totalTokens: int = 0, maxTokens: int = 0):
        '''
        Create an instance of the Place class.
        @param name: Unique name of the Place, must be string
        @param tokens: Current number of tokens held by Place, must be integer
        @param totalTokens: Total number of tokens held by Place for statistics, must be integer        TODO: remove from constructor, it's updated automatically
        @param maxTokens: Maximum number of tokens held by Place for statistics, must be integer        TODO: remove from constructor, it's updated automatically
        '''
        if (checkName(name)):
            # name of the Place, must be unique
            self.name = name

            # number of initial tokens, default 0, if set, totalTokens and maxTokens get the same value
            self.tokens = tokens

            if (tokens == 0):
                # variable to count the total number of tokens in Place for statistics, default 0
                self.totalTokens = totalTokens
            else:
                self.totalTokens = tokens
            if (tokens == 0):
                # variable to count the maximum tokens in Place for statistics, default 0
                self.maxTokens = maxTokens
            else:
                self.maxTokens = tokens

            # list of Input Arcs originating from current Place
            self.inputArcs = []

            # list of Output Arcs targeting the current Place
            self.outputArcs = []

            # list of Inhibitor Arcs originating from current Place
            self.inhibArcs = []

            # add place to PN's Place list
            placeList.append(self)

        else:
            del self
            raise Exception("A Place already exists named: " + name)

    def __str__(self):
        '''
        Default return value of class, gives description of current state of Place.
        '''
        returnString = (
            f"Place (name={self.name}, "
            f"current number of tokens={self.tokens}, "
            f"total tokens held={self.totalTokens}, "
            f"max tokens held={self.maxTokens}, "
            f"list of originating Input Arcs={str(self.inputArcs)}, "
            f"list of targeting Output Arcs={str(self.outputArcs)}, "
            f"list of originating Inhibitor Arcs={str(self.inhibArcs)}, "
        )
        return returnString

    # NAME
    def setName(self, newName: str):
        '''
        Setter function for name of Place.
        @param newName: Unique new name for Place, must be string
        '''
        if (checkName(newName)):
            self.name = newName
        else:
            raise Exception("A Place already exists named: " + newName)

    def getName(self):
        '''
        Getter function for name of Place.
        Returns current name of Place.
        '''
        return self.name

    # TOKENS
    def setTokens(self, tokens: int):
        '''
        Setter function for number of tokens held of Place.
        @param tokens: New value for number of tokens held of Place, must be integer
        '''
        self.tokens = tokens

    def getTokens(self):
        '''
        Getter function for number of tokens held of Place.
        Returns current number of tokens held of Place.
        '''
        return self.tokens

    # TOTAL TOKENS
    def setTotalTokens(self, totalTokens: int):
        '''
        Setter function for total number of tokens held of Place, for statistics.
        @param totalTokens: New value for total number of tokens held of Place, must be integer
        '''
        self.totalTokens = totalTokens

    def getTotalTokens(self):
        '''
        Getter function for total number of tokens held of Place, for statistics.
        Returns current total number of tokens held of Place.
        '''
        return self.totalTokens

    # MAX TOKENS
    def setMaxTokens(self, maxTokens: int):
        '''
        Setter function for maximum number of tokens held of Place, for statistics.
        @param maxTokens: New value for maximum number of tokens held of Place, must be integer
        '''
        self.maxTokens = maxTokens

    def getMaxTokens(self):
        '''
        Getter function for maximum number of tokens held of Place, for statistics.
        Returns current maximum number of tokens held of Place.
        '''
        return self.maxTokens

    # INPUT ARCS
    def setInputArcs(self, *inputArcList):
        '''
        Setter function to overwrite Input Arcs originating from current Place.
        Note: this function deletes existing list of Input Arcs, and creates new list with the given Input Arcs. To add single new Input Arc to Place's Input Arc list, use addInputArc.
        @param *inputArcList: New tuple of Input Arcs to be added to Place's Input Arc list, must be a tuple of instances of class Input Arc
        '''
        for arc in inputArcList:
            if(checkType(arc) != "InputArc"):
                raise Exception(
                    "Place's new Input Arc list's elements must be instances of class Input Arc")
        self.inputArcs.clear
        for arc in inputArcList:
            arc.setFromPlace(self)
            self.inputArcs.append(arc)

    def getInputArcs(self):
        '''
        Getter function for list of Input Arcs originating from current Place.
        Returns current list of Input Arcs originating from current Place.
        '''
        return self.inputArcs

    def addInputArc(self, newInputArc):
        '''
        Setter function to add new Input Arc originating from current Place, to Place's Input Arc list.
        Note: this function adds one new Input Arc to the Place's Input Arc list. To overwrite the list with a tuple of multiple Input Arcs, use setInputArcs.
        @param newInputArc: New Input Arc to be added to Place's Input Arc list, must be instance of class Input Arc
        '''
        if(checkType(newInputArc) != "InputArc"):
            raise Exception(
                "Place's new Input Arc must be instance of class Input Arc")
        newInputArc.setFromPlace(self)
        self.inputArcs.append(newInputArc)

    # OUTPUT ARCS
    def setOutputArcs(self, *outputArcList):
        '''
        Setter function to overwrite Output Arcs targeting current Place.
        Note: this function deletes existing list of Output Arcs, and creates new list with the given Output Arcs. To add single new Output Arc to Place's Output Arc list, use addOutputArcs.
        @param *outputArcList: New tuple of Output Arcs to be added to Place's Output Arc list, must be a tuple of instances of class Output Arc
        '''
        for arc in outputArcList:
            if(checkType(arc) != "OutputArc"):
                raise Exception(
                    "Place's new Output Arc list's elements must be instances of class Output Arc")
        self.outputArcs.clear
        for arc in outputArcList:
            arc.setToPlace(self)
            self.outputArcs.append(arc)

    def getOutputArcs(self):
        '''
        Getter function for list of Output Arcs targeting current Place.
        Returns current list of Output Arcs targeting current Place.
        '''
        return self.outputArcs

    def addOutputArcs(self, newOutputArc):
        '''
        Setter function to add new Output Arc targeting current Place, to Place's Output Arc list.
        Note: this function adds one new Output Arc to the Place's Output Arc list. To overwrite the list with a tuple of multiple Output Arcs, use setOutputArcs.
        @param newOutputArc: New Output Arc to be added to Place's Output Arc list, must be instance of class Output Arc
        '''
        if(checkType(newOutputArc) != "OutputArc"):
            raise Exception(
                "Place's new Output Arc must be instance of class Output Arc")
        newOutputArc.setToPlace(self)
        self.outputArcs.append(newOutputArc)

    # INHIB ARCS
    def setInhibArcs(self, *inhibArcList):
        '''
        Setter function to overwrite Inhibitor Arcs originating from current Place.
        Note: this function deletes existing list of Inhibitor Arcs, and creates new list with the given Inhibitor Arcs. To add single new Inhibitor Arc to Place's Inhibitor Arc list, use addInhibArc.
        @param *inhibArcList: New tuple of Inhibitor Arcs to be added to Place's Inhibitor Arc list, must be a tuple of instances of class Inhibitor Arc
        '''
        for arc in inhibArcList:
            if(checkType(arc) != "InhibArc"):
                raise Exception(
                    "Place's new Inhibitor Arc list's elements must be instances of class Inhibitor Arc")
        self.inhibArcs.clear
        for arc in inhibArcList:
            arc.setOrigin(self)
            self.inhibArcs.append(arc)

    def getInhibArcs(self):
        '''
        Getter function for list of Inhibitor Arcs originating from current Place.
        Returns current list of Inhibitor Arcs originating from current Place.
        '''
        return self.inhibArcs

    def addInhibArc(self, newInhibArc):
        '''
        Setter function to add new Inhibitor Arc originating from current Place, to Place's Inhibitor Arc list.
        Note: this function adds one new Inhibitor Arc to the Place's Inhibitor Arc list. To overwrite the list with a tuple of multiple Inhibitor Arcs, use setInhibArcs.
        @param newInhibArc: New Inhibitor Arc to be added to Place's Inhibitor Arc list, must be instance of class Inhibitor Arc
        '''
        if(checkType(newInhibArc) != "InhibArc"):
            raise Exception(
                "Place's new Inhibitor Arc must be instance of class Inhibitor Arc")
        newInhibArc.setOrigin(self)
        self.inhibArcs.append(newInhibArc)


def checkName(name):
    for place in placeList:
        if (place.name == name):
            return False
    return True


def findPlaceByName(name):
    for place in placeList:
        if (place.name == name):
            return place
    raise Exception('Place does not exists with name: ' + name)


def checkType(object):
    return object.__class__.__name__
