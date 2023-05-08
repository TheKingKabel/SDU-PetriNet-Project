from main.PetriNet import *

# a more advanced PN of the hospital example
# patients are entering to the hospital at random intervals
# upon arrival they check if they can find an empty seat in the Waiting Room
# we have a very small hospital in our town, the Waiting Room has only room for 3 people at a time
# if they see that they can't sit down, they become annoyed and leave the hospital without getting any treatment
# if they can find an empty seat to sit, they wait patiently for their turn to be treated
# treatments last a random amount of time, after that the healthy ex-patients happily leave the hospital
# as additional info, we'd like to know about...
#   1. the downtime of the server (when all seats are taken in the Waiting Room (=3))
#   2. the idling of the server (when no seats are taken in the Waiting Room (=0))
# play around with the setting, parameters and numbers, and see how the results change

hospital = PetriNet("Hospital")

Arrived = Place("Arrived", hospital)
WaitingRoom = Place("WaitingRoom", hospital)
LeaveNoTreat = Place("LeaveNoTreat", hospital)
LeaveTreat = Place("LeaveTreat", hospital)

Arrival = TimedTransition("Arrival", hospital, "EXP",
                          1.0, 5.0, timeUnitType='hr')

# correct syntax of defining guard conditions, callable functions returning boolean values
# this way the function references can still be accessed from other modules, as well as PN temporary (in-simulation) values evaluated dynamically


def CanWaitGuard():
    return WaitingRoom.tokens < 3


def CantWaitGuard():
    return WaitingRoom.tokens >= 3


CanWait = ImmediateTransition("CanWait", hospital, CanWaitGuard)
CantWait = ImmediateTransition("CantWait", hospital, CantWaitGuard)
Treatment = TimedTransition("Treatment", hospital,
                            'NORM', 2.0, 6.0, timeUnitType='hr')

OUTArrivalArrived = OutputArc(
    "OUTArrivalArrived", hospital, Arrival, Arrived)
INPArrivedCanWait = InputArc(
    "INPArrivedCanWait", hospital, Arrived, CanWait)
INPArrivedCantWait = InputArc(
    "INPArrivedCantWait", hospital, Arrived, CantWait)
OUTCantWaitLeaveNoTreat = OutputArc(
    "OUTCantWaitLeaveNoTreat", hospital, CantWait, LeaveNoTreat)
OUTCanWaitWaitingRoom = OutputArc(
    "OUTCanWaitWaitingRoom", hospital, CanWait, WaitingRoom)
INPWaitingRoomTreatment = InputArc(
    "INPWaitingRoomTreatment", hospital, WaitingRoom, Treatment)
OUTTreatmentLeaveTreat = OutputArc(
    "OUTTreatmentLeaveTreat", hospital, Treatment, LeaveTreat)

# correct syntax of defining conditions, callable functions returning boolean values
# this way the function references can still be accessed from other modules, as well as PN temporary (in-simulation) values evaluated dynamically


def roomFull():
    return WaitingRoom.tokens == 3


def roomEmpty():
    return WaitingRoom.tokens == 0


hospital.runSimulations(5, 80, 1, 1337, 'hr', [(
    'Waiting room is full', .05, roomFull), ('Waiting room is empty', .05, roomEmpty)])
