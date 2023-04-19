from main.PetriNet import *

bank = PetriNet("Bank")

TEnter = TimedTransition("TEnter", bank, "NORM", 5.0, 25.0, timeUnitType='min')
TWait = ImmediateTransition("TWait", bank)
TService = TimedTransition("TService", bank, 'NORM',
                           0.17, 0.6, timeUnitType='hr')

PQueue = Place("PQueue", bank, 2)
PService = Place("PService", bank, 1)

OUTTEnterPQueue = OutputArc("OUTTEnterPQueue", bank, TEnter, PQueue)
OUTTWaitPService = OutputArc("OUTTWaitPService", bank, TWait, PService)

INPPQueueTWait = InputArc("INPPQueueTWait", bank, PQueue, TWait)
INPPServiceTService = InputArc("INPPServiceTService", bank, PService, TService)

INHPServiceTWait = InhibArc("INHPServiceTWait", bank, PService, TWait)


def serverBusy():
    return PService.tokens >= 1


def bigQueue():
    return PQueue.tokens >= 4


def exactQueue():
    return PQueue.tokens == 2


bank.runSimulation(6, defTimeUnit='hr', conditionals=[
                   ('Busy bank teller', serverBusy), ('Lot of customers', bigQueue), ('Queue of customers is exactly 2', exactQueue)])

# bank.describe()
