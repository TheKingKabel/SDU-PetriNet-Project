from main import instantTransList

class InstantTransition:

    def __init__(self, name: str, enabled: bool = True, fireProbability: float = 1.0, fireCount: int = 0):
        if (checkName(name)):
            self.name = name                        # name of the immediate transition
            self.enabled = enabled                  # immediate transition enabled for firing, default: true
            self.fireProbability = fireProbability  # probability of firing, default 1.0 (100%)
            self.fireCount = fireCount              # number of times immediate transition has fired, default 0

            #TODO: other arguments?

            instantTransList.append(self)

        else:
            del self
            raise Exception("An Immediate Transition already exists named: " + name)

    def __str__(self):
        returnString = (
            f"Immediate Transition (name={self.name}, "
            f"enabled={self.enabled}, "
            f"firing probability={self.fireProbability}, "
            f"times fired={self.fireCount}"
        )
        return returnString

    def setName(self, newName: str):
        if (checkName(newName)):
            self.name = newName
        else:
            raise Exception("An Immediate Transition already exists named: " + newName)

    def getName(self):
        return self.name

    def setEnable(self, enabled: bool):
        self.enabled = enabled

    def getEnable(self):
        return self.enabled

    def setFireProbability(self, fireProbability: float):
        self.fireProbability = fireProbability

    def getFireProbability(self):
        return self.fireProbability
    
    def setFireCount(self, fireCount: int):
        self.fireCount = fireCount

    def getFireCount(self):
        return self.fireCount

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


def setName(transName: str, newName: str):
    trans = findTransitionByName(transName)
    if (checkName(newName)):
        trans.name = newName
    else:
        raise Exception("An Immediate Transition already exists named: " + newName)

def getName(transName: str):
    trans = findTransitionByName(transName)
    return trans.name

def setEnabled(transName: str, enabled: bool):
    trans = findTransitionByName(transName)
    trans.enabled = enabled

def getEnabled(transName: str):
    trans = findTransitionByName(transName)
    return trans.enabled

def setFireProbability(transName: str, fireProbability: float):
    trans = findTransitionByName(transName)
    trans.fireProbability = fireProbability

def getFireProbability(transName: str, fireProbability: float):
    trans = findTransitionByName(transName)
    trans.fireProbability = fireProbability

def setFireCount(transName: str, fireCount: int):
    trans = findTransitionByName(transName)
    trans.fireCount = fireCount

def getFireCount(transName: str):
    trans = findTransitionByName(transName)
    return trans.fireCount