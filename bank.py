from components.timedTransition import *
from components.place import *
from components.outputArc import *
from components.instantTransition import *
from components.inhibArc import *
from components.inputArc import *
from main import *


T_Enter = TimedTransition("T_Enter","normal","race")
Queue = Place("Queue")                                        # Test: set tokens to 2
T_EnterQueueTrans = OutputArc("T_EnterQueueTrans", T_Enter, Queue)
T_Wait = InstantTransition("T_Wait")
QueueT_WaitTrans =InputArc("QueueT_WaitTrans", Queue, T_Wait)
Service = Place("Service")                                    # Test: set tokens to 1
T_WaitServiceInhib = InhibArc("WaitBlock", Service, T_Wait)
T_WaitServiceTrans = OutputArc("T_WaitServiceTrans", T_Wait, Service)
T_Service = TimedTransition("T_Service", "normal", "race")
ServiceT_ServiceTrans = InputArc("ServiceT_ServiceTrans", Service, T_Service)

print("Places:")
getPlaces()
print("Timed Transitions:")
getTimedTransitions()
print("Immediate Transitions:")
getInstantTransitions()
print("Input Edges:")
getInputEdges()
print("Output Edges:")
getOutputEdges()
print("Inhibitor Edges:")
getInhibEdges()