from main.PetriNet import *

# a basic Mutually Exclusive experiment with PN modelling
# taking IT1 or IT2 (competing) Immediate Transitions is a coin flip (50-50%) decision

mutex = PetriNet("MUTEX compete")

Choice = Place("Choice", mutex, 50)

IT1 = ImmediateTransition("IT1", mutex, None, 0.5)
IT2 = ImmediateTransition("IT2", mutex, None, 0.5)

IA1 = InputArc("IA1", mutex, Choice, IT1)
IA2 = InputArc("IA2", mutex, Choice, IT2)

Wait1 = Place("Wait1", mutex)
Wait2 = Place("Wait2", mutex)

OA1 = OutputArc("OA1", mutex, IT1, Wait1)
OA2 = OutputArc("OA2", mutex, IT2, Wait2)

TT1 = TimedTransition("TT1", mutex, 'NORM', 1.0, 3.0)
TT2 = TimedTransition("TT2", mutex, 'NORM', 1.0, 3.0)

IA21 = InputArc("IA21", mutex, Wait1, TT1)
IA22 = InputArc("IA22", mutex, Wait2, TT2)

OA21 = OutputArc("OA21", mutex, TT1, Choice)
OA22 = OutputArc("OA22", mutex, TT2, Choice)

mutex.runSimulations(10, 50)
