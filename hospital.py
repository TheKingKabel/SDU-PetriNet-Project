from main.PetriNet import *

# a more advanced PN of the hospital example
# patients are entering to the hospital at random intervals
# upon arrival they check if they can find an empty seat in the Waiting Room
# we have a very small hospital in our town,
# the Waiting Room has only room for 3 people at a time
# if they see that they can't sit down,
# they become annoyed and leave the hospital without getting any treatment
# if they can find an empty seat to sit, they wait patiently for their turn to be treated
# treatments last a random amount of time,
# after that the healthy ex-patients happily leave the hospital
# as additional info, we'd like to know about...
#   1. the downtime of the server (when all seats are taken in the Waiting Room (=3))
#   2. the idling of the server (when no seats are taken in the Waiting Room (=0))
# play around with the setting, parameters and numbers, and see how the results change

Hospital = PetriNet("Hospital")

Arrived = Place("Arrived", Hospital)
WaitingRoom = Place("WaitingRoom", Hospital)
LeaveNoTreat = Place("LeaveNoTreat", Hospital)
LeaveTreat = Place("LeaveTreat", Hospital)

Arrival = TimedTransition("Arrival", Hospital, "EXP",
                          1.0, 5.0, timeUnitType='hr')

# correct syntax of defining guard conditions, callable functions returning boolean values
# this way the function references can still be accessed from other modules,
# as well as PN temporary (in-simulation) values evaluated dynamically


def CanWaitGuard():
    return findPetriNetByName("Hospital").findPlaceByName("WaitingRoom").tokens < 3


def CantWaitGuard():
    return findPetriNetByName("Hospital").findPlaceByName("WaitingRoom").tokens >= 3


CanWait = ImmediateTransition("CanWait", Hospital, CanWaitGuard)
CantWait = ImmediateTransition("CantWait", Hospital, CantWaitGuard)
Treatment = TimedTransition("Treatment", Hospital,
                            'NORM', 2.0, 6.0, timeUnitType='hr')

OUTArrivalArrived = OutputArc(
    "OUTArrivalArrived", Hospital, Arrival, Arrived)
INPArrivedCanWait = InputArc(
    "INPArrivedCanWait", Hospital, Arrived, CanWait)
INPArrivedCantWait = InputArc(
    "INPArrivedCantWait", Hospital, Arrived, CantWait)
OUTCantWaitLeaveNoTreat = OutputArc(
    "OUTCantWaitLeaveNoTreat", Hospital, CantWait, LeaveNoTreat)
OUTCanWaitWaitingRoom = OutputArc(
    "OUTCanWaitWaitingRoom", Hospital, CanWait, WaitingRoom)
INPWaitingRoomTreatment = InputArc(
    "INPWaitingRoomTreatment", Hospital, WaitingRoom, Treatment)
OUTTreatmentLeaveTreat = OutputArc(
    "OUTTreatmentLeaveTreat", Hospital, Treatment, LeaveTreat)

# correct syntax of defining conditions,
# callable functions returning boolean values
# this way the function references can still be accessed from other modules,
# as well as PN temporary (in-simulation) values evaluated dynamically


def roomFull():
    return WaitingRoom.tokens == 3


def roomEmpty():
    return WaitingRoom.tokens == 0


Hospital.runSimulations(5, 80, 1, 1337, 'hr', [
    ('Waiting room is full', .05, roomFull),
    ('Waiting room is empty', .05, roomEmpty)])
