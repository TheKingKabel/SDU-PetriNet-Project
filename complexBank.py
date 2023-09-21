from main.PetriNet import *

# a more advanced version of the bank example
# created for thesis example

complexBank = PetriNet("BigBank")

WaitingLine = Place("WaitingLine", complexBank)
Service1 = Place("Service1", complexBank)
Service2 = Place("Service2", complexBank)


def WaitingLineFull():
    return findPetriNetByName("BigBank").findPlaceByName("WaitingLine").tokens > 3


def BankTeller1Busy():
    return findPetriNetByName("BigBank").findPlaceByName("Service1").tokens == 1


Enter = TimedTransition("Enter", complexBank, "NORM",
                        2.0, 1.5, timeUnitType='min')
CanWait1 = ImmediateTransition("CanWait1", complexBank)
CanWait2 = ImmediateTransition("CanWait2", complexBank, BankTeller1Busy)

CantWait = ImmediateTransition("CantWait", complexBank, WaitingLineFull)
BankTeller1 = TimedTransition(
    "BankTeller1", complexBank, 'NORM', 0.083, 0.05, timeUnitType='hr')
BankTeller2 = TimedTransition("BankTeller2", complexBank,
                              'UNI', 4.0, 10.0, timeUnitType='min')

OA_EnterWaitingLine = OutputArc(
    "OA_EnterWaitingLine", complexBank, Enter, WaitingLine)

IA_WaitingLineCanWait1 = InputArc(
    "IA_WaitingLineCanWait1", complexBank, WaitingLine, CanWait1)
IA_WaitingLineCanWait2 = InputArc(
    "IA_WaitingLineCanWait2", complexBank, WaitingLine, CanWait2)
IA_WaitingLineCantWait = InputArc(
    "IA_WaitingLineCantWait", complexBank, WaitingLine, CantWait)

OA_CanWait1Service1 = OutputArc(
    "OA_CanWait1Service1", complexBank, CanWait1, Service1)
OA_CanWait1Service2 = OutputArc(
    "OA_CanWait1Service2", complexBank, CanWait2, Service2)

INHA_Service1CanWait1 = InhibArc(
    "INHA_Service1CanWait1", complexBank, Service1, CanWait1)
INHA_Service1CanWait2 = InhibArc(
    "INHA_Service1CanWait2", complexBank, Service2, CanWait2)

IA_Service1BankTeller1 = InputArc(
    "IA_Service1BankTeller1", complexBank, Service1, BankTeller1)
IA_Service2BankTeller2 = InputArc(
    "IA_Service2BankTeller2", complexBank, Service2, BankTeller2)

# conditional functions


def BothServersBusy():
    return (findPetriNetByName("BigBank").findPlaceByName("Service1").tokens == 1) and (findPetriNetByName("BigBank").findPlaceByName("Service2").tokens == 1)


def QueueIsFull():
    return findPetriNetByName("BigBank").findPlaceByName("WaitingLine").tokens == 3


def Service2Idle():
    return findPetriNetByName("BigBank").findPlaceByName("Service2").tokens == 0


complexBank.runSimulations(100, 480, 1, 1337, defTimeUnit='min', conditionals=[
    ('Both bank tellers are busy', .05, BothServersBusy),
    ('Waiting line is full', .10, QueueIsFull),
    ('Bank teller 2 is idle', .15, Service2Idle)])
