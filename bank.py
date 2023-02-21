from PetriNet import *

bank = PetriNet("bank")

TEnter = TimedTransition("TEnter", bank, "normal", "race")
TWait = ImmediateTransition("TWait", bank)
TService = TimedTransition("TService", bank, "normal", "race")

PQueue = Place("PQueue", bank, 2)
PService = Place("PService", bank)

OUTTEnterPQueue = OutputArc("OUTTEnterPQueue", bank, TEnter, PQueue)
OUTTWaitPService = OutputArc("OUTTWaitPService", bank, TWait, PService)

INPPQueueTWait = InputArc("INPPQueueTWait", bank, PQueue, TWait)
INPPServiceTService = InputArc("INPPServiceTService", bank, PService, TService)

INHPServiceTWait = InhibArc("INHPServiceTWait", bank, PService, TWait)


bank.describe()
