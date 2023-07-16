from main.PetriNet import *

loadBank = loadExistingPN("logs\Bank\Bank_PetriNet.pnml", "loadBank")

loadBank.describe()


def serverBusy():
    return loadBank.findPlaceByName("PService").tokens >= 1


def bigQueue():
    return loadBank.findPlaceByName("PQueue").tokens >= 4


def exactQueue():
    return loadBank.findPlaceByName("PQueue").tokens == 2


loadBank.runSimulations(10, 8, 1, 1337, defTimeUnit='hr', conditionals=[
    ('Busy bank teller', .05, serverBusy), ('Lot of customers', .10, bigQueue), ('Queue of customers is exactly 2', .15, exactQueue)])
