from main.PetriNet import *

bank = PetriNet("Bank")

TEnter = TimedTransition("TEnter", bank, "NORM", 1.0, 10.0)
TWait = ImmediateTransition("TWait", bank)
TService = TimedTransition("TService", bank, 'NORM', 2.5, 8.5)

PQueue = Place("PQueue", bank, 2)
PService = Place("PService", bank, 1)

OUTTEnterPQueue = OutputArc("OUTTEnterPQueue", bank, TEnter, PQueue)
OUTTWaitPService = OutputArc("OUTTWaitPService", bank, TWait, PService)

INPPQueueTWait = InputArc("INPPQueueTWait", bank, PQueue, TWait)
INPPServiceTService = InputArc("INPPServiceTService", bank, PService, TService)

INHPServiceTWait = InhibArc("INHPServiceTWait", bank, PService, TWait)


bank.runSimulation(35)

bank.describe()
