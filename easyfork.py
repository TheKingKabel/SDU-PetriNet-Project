from main.PetriNet import *

fork = PetriNet("Easy Forking")

Start = Place("Start", fork, 1)

IT1 = ImmediateTransition("IT1", fork)

IA1 = InputArc("IA1", fork, Start, IT1)

Ready = Place("Ready", fork)

Wait = Place("Wait", fork)

OA1 = OutputArc("OA1", fork, IT1, Ready)
OA2 = OutputArc("OA2", fork, IT1, Wait)

TT1 = TimedTransition("TT1", fork, 'NORM', 1.0, 5.0)

IA2 = InputArc("IA2", fork, Wait, TT1)

Done = Place("Done", fork)

OA3 = OutputArc("OA3", fork, TT1, Done)

IT2 = ImmediateTransition("IT2", fork)

Finish = Place("Finish", fork)

IA3 = InputArc("IA3", fork, Done, IT2)
IA4 = InputArc("IA4", fork, Ready, IT2)

OA4 = OutputArc("OA4", fork, IT2, Finish)

fork.runSimulation(20)
