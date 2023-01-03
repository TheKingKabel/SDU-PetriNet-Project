from main import transList

class Transition:

    def __init__(self, name: str, distType, agePolicy, enabled: bool = True, fireCount: int = 0):
        if (checkName(name)):
            self.name = name #name of the transition
            self.distType = distType #TODO: type of distribution
            self.enabled = enabled #transition enabled for firing, default: true
            self.agePolicy = agePolicy #TODO: race anabled/disabled
            self.fireCount = fireCount #number of times transition has fired, default 0

            #TODO: other arguments?

            transList.append(self)

        else:
            del self
            raise Exception("A Transition already exists named: " + name)

    def __str__(self):
        return f'Transition (name={self.name}, distribution type={self.distType}, enabled={self.enabled}, times fired={self.fireCount}'

    def setName(self, newName: str):
        if (checkName(newName)):
            self.name = newName
        else:
            raise Exception("A Transition already exists named: " + newName)

    def getName(self):
        return self.name
    
    def setDistType(self, distType):
        self.distType = distType

    def getDistType(self):
        return self.distType

    def setEnable(self, enabled: bool):
        self.enabled = enabled

    def getEnable(self):
        return self.enabled

    def setAgePolicy(self, agePolicy):
        self.agePolicy = agePolicy

    def getAgePolicy(self):
        return self.agePolicy
    
    def setFireCount(self, fireCount: int):
        self.fireCount = fireCount

    def getFireCount(self):
        return self.fireCount

def checkName(name):
    for trans in transList:
        if (trans.name == name):
            return False
    return True

def findTransitionByName(name):
    for trans in transList:
        if (trans.name == name):
            return trans
    raise Exception('Transition does not exists with name: ' + name)


def setName(transName: str, newName: str):
    trans = findTransitionByName(transName)
    if (checkName(newName)):
        trans.name = newName
    else:
        raise Exception("A Transition already exists named: " + newName)

def getName(transName: str):
    trans = findTransitionByName(transName)
    return trans.name
    
def setDistType(transName: str, distType):
    trans = findTransitionByName(transName)
    trans.distType = distType

def getDistType(transName: str):
    trans = findTransitionByName(transName)
    return trans.distType

def setAgePolicy(transName: str, agePolicy):
    trans = findTransitionByName(transName)
    trans.agePolicy = agePolicy

def getAgePolicy(transName: str):
    trans = findTransitionByName(transName)
    return trans.agePolicy

def setEnabled(transName: str, enabled: bool):
    trans = findTransitionByName(transName)
    trans.enabled = enabled

def getEnabled(transName: str):
    trans = findTransitionByName(transName)
    return trans.enabled

def setFireCount(transName: str, fireCount: int):
    trans = findTransitionByName(transName)
    trans.fireCount = fireCount

def getFireCount(transName: str):
    trans = findTransitionByName(transName)
    return trans.fireCount