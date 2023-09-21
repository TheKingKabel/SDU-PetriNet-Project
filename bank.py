from main.PetriNet import *

# a more advanced version of the bank example
# customers are entering the banks via TEnter at random intervals
# one bank clerk is servicing them which takes a random amount of time for him too
# as additional info, we'd like to know about...
#   1. the downtime of the server (when out bank teller is busy)
#   2. the occurrences of a 'big queue' accumulating in our small bank ("Four's a Crowd")
#   3. the times the queue is exactly 2 people waiting for their turns


# definition of PN, following recommended structure and typing
bank = PetriNet("Bank")

TEnter = TimedTransition("TEnter", bank, "NORM", 5.0, 25.0, timeUnitType='min')
TWait = ImmediateTransition("TWait", bank)
TService = TimedTransition("TService", bank, 'NORM',
                           0.083, 0.25, timeUnitType='hr')

PQueue = Place("PQueue", bank, 2)
PService = Place("PService", bank, 1)

OUTTEnterPQueue = OutputArc("OUTTEnterPQueue", bank, TEnter, PQueue)
OUTTWaitPService = OutputArc("OUTTWaitPService", bank, TWait, PService)

INPPQueueTWait = InputArc("INPPQueueTWait", bank, PQueue, TWait)


def getPServiceTokens():
    if (PService.tokens == 0):
        return 1
    else:
        return PService.tokens


INServiceTService = InputArc(
    "INServiceTService", bank, PService, TService, getPServiceTokens)

INHPServiceTWait = InhibArc("INHPServiceTWait", bank, PService, TWait)

# correct syntax of defining conditionals, callable functions returning boolean values
# this way the function references can still be accessed from other modules,
# as well as PN temporary (in-simulation) values evaluated dynamically


# an advanced simulations method call
# will run 10 simulations (or replications)
# each simulation run will last 8 set time units...
# (the verbosity of the logs is set to be 1: medium setting,
# resulting in no log generation into the terminal,
# but all files are generated into the folders)
# ...which is in this case not the default 'sec' (seconds),
# but rather 'hr' hours
# we're passing the conditionals following this struct structure:
# list[tuple1('conditional description', alpha value, function reference), tuple2(...),...]
# type checks are implemented thoroughly,
# invalid input will not execute but return Exception

# conditional functions
def serverBusy():
    return PService.tokens >= 1


def bigQueue():
    return PQueue.tokens >= 4


def exactQueue():
    return PQueue.tokens == 2


bank.runSimulations(10, 8, 1, 1337, defTimeUnit='hr', conditionals=[
                   ('Busy bank teller', .05, serverBusy),
                   ('Lot of customers', .10, bigQueue),
                   ('Queue of customers is exactly 2', .15, exactQueue)])

# calling this function dumps the same human-readable PN description
# that can be found in <setPath>/logs/<PetriNet name>/<PetriNet name>_PetriNet.txt
bank.describe()
