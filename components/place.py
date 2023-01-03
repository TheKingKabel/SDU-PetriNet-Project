from main import placeList

class Place:

    def __init__(self, name: str, start: bool=False, tokens: int=0, totalTokens: int=0, maxTokens: int=0):
        if (checkName(name)):
            self.name = name #name of the place
            self.start = start #start place, default false
            self.tokens = tokens #nbr of initial tokens, default 0, if set, totalTokens and maxTokens get the same value
            if (tokens == 0):
                self.totalTokens = totalTokens #var used to count the total number of tokens in place, default 0
            else:
                self.totalTokens = tokens
            if (tokens == 0):
                self.maxTokens = maxTokens # var used to count the maximum tokens in place, default 0
            else:
                self.maxTokens = tokens

            placeList.append(self)

        else:
            del self
            raise Exception("A Place already exists named: " + name)

    def __str__(self):
        return f'Place (name={self.name}, start place={self.start}, current nbr of tokens={self.tokens}, total tokens held={self.totalTokens}, max tokens held={self.maxTokens}'

    def setName(self, newName: str):
        if (checkName(newName)):
            self.name = newName
        else:
            raise Exception("A Place already exists named: " + newName)
    
    def getName(self):
        return self.name
    
    def setStart(self, start: bool):
        self.start = start

    def getStart(self):
        return self.start

    def setTokens(self, tokens: int):
        self.tokens = tokens

    def getTokens(self):
        return self.tokens
    
    def setTotalTokens(self, totalTokens: int):
        self.totalTokens = totalTokens

    def getTotalTokens(self):
        return self.totalTokens

    def setMaxTokens(self, maxTokens: int):
        self.maxTokens = maxTokens

    def getMaxTokens(self):
        return self.maxTokens

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


def setName(placeName: str, newName: str):
    place = findPlaceByName(placeName)
    if (checkName(newName)):
        place.name = newName
    else:
        raise Exception("A Place already exists named: " + newName)

def getName(placeName: str):
    place = findPlaceByName(placeName)
    return place.name
    
def setStart(placeName: str, start: bool):
    place = findPlaceByName(placeName)
    place.start = start

def getStart(placeName: str):
    place = findPlaceByName(placeName)
    return place.start

def setTokens(placeName: str, tokens: int):
    place = findPlaceByName(placeName)
    place.tokens = tokens

def getTokens(placeName: str):
    place = findPlaceByName(placeName)
    return place.tokens
    
def setTotalTokens(placeName: str, totalTokens: int):
    place = findPlaceByName(placeName)
    place.totalTokens = totalTokens

def getTotalTokens(placeName: str):
    place = findPlaceByName(placeName)
    return place.totalTokens

def setMaxTokens(placeName: str, maxTokens: int):
    place = findPlaceByName(placeName)
    place.maxTokens = maxTokens

def getMaxTokens(placeName: str):
    place = findPlaceByName(placeName)
    return place.maxTokens