from PetriNet import *
from simulation import runSimulation

bank = PetriNet("bank")

TEnter = TimedTransition("TEnter", bank, "NORM")
TWait = ImmediateTransition("TWait", bank)
TService = TimedTransition("TService", bank)

PQueue = Place("PQueue", bank, 2)
PService = Place("PService", bank)

OUTTEnterPQueue = OutputArc("OUTTEnterPQueue", bank, TEnter, PQueue)
OUTTWaitPService = OutputArc("OUTTWaitPService", bank, TWait, PService)

INPPQueueTWait = InputArc("INPPQueueTWait", bank, PQueue, TWait)
INPPServiceTService = InputArc("INPPServiceTService", bank, PService, TService)

INHPServiceTWait = InhibArc("INHPServiceTWait", bank, PService, TWait)


runSimulation(bank, 5)

bank.describe()
