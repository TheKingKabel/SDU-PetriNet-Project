from PetriNet import *
from simulation import runSimulation

hospital = PetriNet("Hospital")

Arrived = Place("Arrived", hospital)
WaitingRoom = Place("WaitingRoom", hospital)
LeaveNoTreat = Place("LeaveNoTreat", hospital)
LeaveTreat = Place("LeaveTreat", hospital)

Arrival = TimedTransition("Arrival", hospital, "EXP", 1.0, 5.0)


def CanWaitGuard():
    return WaitingRoom.tokens < 3


def CantWaitGuard():
    return WaitingRoom.tokens >= 3


CanWait = ImmediateTransition("CanWait", hospital, CanWaitGuard)
CantWait = ImmediateTransition("CantWait", hospital, CantWaitGuard)
Treatment = TimedTransition("Treatment", hospital, 'NORM', 2.0, 4.5)

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

runSimulation(hospital, 60)

hospital.describe()
