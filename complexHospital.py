from main.PetriNet import *

# a more advanced version of the hospital example
# created for thesis example

# Petri Net
complexHospital = PetriNet("ComplexHospital")

# Arrivals
NormalArrival = TimedTransition(
    "NormalArrival", complexHospital, 'EXP', 0.0, 5.0, timeUnitType='min')
ImpArrival = TimedTransition(
    "ImpArrival", complexHospital, 'EXP', 0.0, 15.0, timeUnitType='min')

# Arrival places
NormalArrived = Place("NormalArrived", complexHospital)
ImpArrived = Place("ImpArrived", complexHospital)

# Arrivals -> Arrival places
OUT_NormalArrival_NormalArrived = OutputArc(
    "OUT_NormalArrival_NormalArrived", complexHospital, NormalArrival, NormalArrived)
OUT_ImpArrival_ImpArrived = OutputArc(
    "OUT_ImpArrival_ImpArrived", complexHospital, ImpArrival, ImpArrived)

# Waiting Queues
WaitingRoom = Place("WaitingRoom", complexHospital)
LuxuryLounge = Place("LuxuryLounge", complexHospital)

# Wait Or Leave guards


def WaitingRoomFull():
    return findPetriNetByName("ComplexHospital").findPlaceByName("WaitingRoom").tokens == 10


def WaitingRoomFree():
    return findPetriNetByName("ComplexHospital").findPlaceByName("WaitingRoom").tokens < 10


def LuxuryLoungeFull():
    return findPetriNetByName("ComplexHospital").findPlaceByName("LuxuryLounge").tokens == 3


def LuxuryLoungeFree():
    return findPetriNetByName("ComplexHospital").findPlaceByName("LuxuryLounge").tokens < 3


# Wait Or Leave
NormalCanWait = ImmediateTransition(
    "NormalCanWait", complexHospital, WaitingRoomFree)
ImpCanWait = ImmediateTransition(
    "ImpCanWait", complexHospital, LuxuryLoungeFree)

NormalCantWait = ImmediateTransition(
    "NormalCantWait", complexHospital, WaitingRoomFull)
ImpCantWait = ImmediateTransition(
    "ImpCantWait", complexHospital, LuxuryLoungeFull)

# Arrived places -> Wait Or Leave
INP_NormalArrived_NormalCanWait = InputArc(
    "INP_NormalArrived_NormalCanWait", complexHospital, NormalArrived, NormalCanWait)
INP_NormalArrived_NormalCantWait = InputArc(
    "INP_NormalArrived_NormalCantWait", complexHospital, NormalArrived, NormalCantWait)

INP_ImpArrived_ImpCanWait = InputArc(
    "INP_ImpArrived_ImpCanWait", complexHospital, ImpArrived, ImpCanWait)
INP_ImpArrived_ImpCantWait = InputArc(
    "INP_ImpArrived_ImpCantWait", complexHospital, ImpArrived, ImpCantWait)

# CanWait -> Waiting areas
OUT_NormalCanWait_WaitingRoom = OutputArc(
    "OUT_NormalCanWait_WaitingRoom", complexHospital, NormalCanWait, WaitingRoom)
OUT_ImpCanWait_LuxuryLounge = OutputArc(
    "OUT_ImpCanWait_LuxuryLounge", complexHospital, ImpCanWait, LuxuryLounge)

# Doctor Places
DoctorIdle = Place("DoctorIdle", complexHospital, 1)
DoctorWorking = Place("DoctorWorking", complexHospital)

# Can Enter Treatment
NormalCanTreat = ImmediateTransition("NormalCanTreat", complexHospital)
ImpCanTreat = ImmediateTransition("ImpCanTreat", complexHospital)

# VIP Priority
INH_LuxuryLounge_NormalCanTreat = InhibArc(
    "INH_LuxuryLounge_NormalCanTreat", complexHospital, LuxuryLounge, NormalCanTreat)

# Waiting areas -> Can enter treatment
INP_WaitingRoom_NormalCanTreat = InputArc(
    "INP_WaitingRoom_NormalCanTreat", complexHospital, WaitingRoom, NormalCanTreat)
INP_LuxuryLounge_ImpCanTreat = InputArc(
    "INP_LuxuryLounge_ImpCanTreat", complexHospital, LuxuryLounge, ImpCanTreat)

INP_DoctorIdle_NormalCanTreat = InputArc(
    "INP_DoctorIdle_NormalCanTreat", complexHospital, DoctorIdle, NormalCanTreat)
INP_DoctorIdle_ImpCanTreat = InputArc(
    "INP_DoctorIdle_ImpCanTreat", complexHospital, DoctorIdle, ImpCanTreat)

# Being treated
NormalTreating = Place("NormalTreating", complexHospital)
ImpTreating = Place("ImpTreating", complexHospital)

# Can enter treatment -> Being treated
OUT_NormalCanTreat_NormalTreating = OutputArc(
    "OUT_NormalCanTreat_NormalTreating", complexHospital, NormalCanTreat, NormalTreating)
OUT_ImpCanTreat_ImpTreating = OutputArc(
    "OUT_ImpCanTreat_ImpTreating", complexHospital, ImpCanTreat, ImpTreating)

# Treatment
NormalTreatment = TimedTransition(
    "NormalTreatment", complexHospital, 'NORM', 4.5, 2.0, timeUnitType='min')
ImpTreatment = TimedTransition(
    "ImpTreatment", complexHospital, 'NORM', 6.0, 2.0, timeUnitType='min')

# Doctor treating
OUT_NormalCanTreat_DoctorWorking = OutputArc(
    "OUT_NormalCanTreat_DoctorWorking", complexHospital, NormalCanTreat, DoctorWorking)
OUT_ImpCanTreat_DoctorWorking = OutputArc(
    "OUT_ImpCanTreat_DoctorWorking", complexHospital, ImpCanTreat, DoctorWorking)

INP_DoctorWorking_NormalTreatment = InputArc(
    "INP_DoctorWorking_NormalTreatment", complexHospital, DoctorWorking, NormalTreatment)
INP_DoctorWorking_ImpTreatment = InputArc(
    "INP_DoctorWorking_ImpTreatment", complexHospital, DoctorWorking, ImpTreatment)

# Being treated -> Treatment
INP_NormalTreating_NormalTreatment = InputArc(
    "INP_NormalTreating_NormalTreatment", complexHospital, NormalTreating, NormalTreatment)
INP_ImpTreating_ImpTreatment = InputArc(
    "INP_ImpTreating_ImpTreatment", complexHospital, ImpTreating, ImpTreatment)

# Treatment -> Doctor free
OUT_NormalTreatment_DoctorIdle = OutputArc(
    "OUT_NormalTreatment_DoctorIdle", complexHospital, NormalTreatment, DoctorIdle)
OUT_ImpTreatment_DoctorIdle = OutputArc(
    "OUT_ImpTreatment_DoctorIdle", complexHospital, ImpTreatment, DoctorIdle)


# Conditional functions

def DoctorUsage():
    return findPetriNetByName("ComplexHospital").findPlaceByName("DoctorWorking").tokens == 1


def WaitingRoomUsage():
    return findPetriNetByName("ComplexHospital").findPlaceByName("WaitingRoom").tokens >= 1


def WaitingRoomFull():
    return findPetriNetByName("ComplexHospital").findPlaceByName("WaitingRoom").tokens == 10


def LuxuryLoungeUsage():
    return findPetriNetByName("ComplexHospital").findPlaceByName("LuxuryLounge").tokens >= 1


def LuxuryLoungeFull():
    return findPetriNetByName("ComplexHospital").findPlaceByName("LuxuryLounge").tokens == 3


complexHospital.runSimulations(100, 1440, 1, 1337, defTimeUnit='min', conditionals=[
    ('The lone doctor is working', .05, DoctorUsage),
    ('The waiting room is being used', .05, WaitingRoomUsage),
    ('The waiting room is at maximum capacity', .05, WaitingRoomFull),
    ('The luxury lounge is being used', .05, LuxuryLoungeUsage),
    ('The luxury lounge is at maximum capacity', .05, LuxuryLoungeFull)])
