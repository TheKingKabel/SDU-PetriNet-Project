from main.PetriNet import *

# a very simple and straightforward version of the bank example
# customers are entering the banks via TEnter at random intervals
# one bank clerk is servicing them which takes a random amount of time for him too
# change the parameters (including the set seed!) and see how the results change

# bank = PetriNet("SimpleBank")

bank = createNewPN("SimpleBank")

TEnter = TimedTransition("TEnter", bank, "NORM", 5.0, 25.0, timeUnitType='min')
TWait = ImmediateTransition("TWait", bank)
TService = TimedTransition("TService", bank, 'NORM',
                           0.083, 0.25, timeUnitType='hr')

PQueue = Place("PQueue", bank, 2)
PService = Place("PService", bank, 1)

OUTTEnterPQueue = OutputArc("OUTTEnterPQueue", bank, TEnter, PQueue)
OUTTWaitPService = OutputArc("OUTTWaitPService", bank, TWait, PService)

INPPQueueTWait = InputArc("INPPQueueTWait", bank, PQueue, TWait)
INPPServiceTService = InputArc("INPPServiceTService", bank, PService, TService)

INHPServiceTWait = InhibArc("INHPServiceTWait", bank, PService, TWait)

bank.runSimulations(5, 2, randomSeed=1337, defTimeUnit='hr')

# bank.describe()
