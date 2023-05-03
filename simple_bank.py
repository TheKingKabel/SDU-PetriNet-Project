from main.PetriNet import *

bank = PetriNet("SimpleBank")

TEnter = TimedTransition("TEnter", bank, "NORM", 5.0, 25.0, timeUnitType='min')
TWait = ImmediateTransition("TWait", bank)
TService = TimedTransition("TService", bank, 'NORM',
                           0.083, 0.25, timeUnitType='hr')

PQueue = Place("PQueue", bank, 3)
PService = Place("PService", bank, 1)

OUTTEnterPQueue = OutputArc("OUTTEnterPQueue", bank, TEnter, PQueue)
OUTTWaitPService = OutputArc("OUTTWaitPService", bank, TWait, PService)

INPPQueueTWait = InputArc("INPPQueueTWait", bank, PQueue, TWait)
INPPServiceTService = InputArc("INPPServiceTService", bank, PService, TService)

INHPServiceTWait = InhibArc("INHPServiceTWait", bank, PService, TWait)


# bank.runSimulations(10, 6, 0, defTimeUnit='hr')
bank.runSimulations(2, 1, 1, 1337, defTimeUnit='hr')

# bank.describe()
