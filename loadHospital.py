from main.PetriNet import *

loadHospital = loadExistingPN(
    "logs\Hospital\Hospital_PetriNet.pnml", "Hospital")

loadHospital.describe()


def roomFull():
    return findPetriNetByName("Hospital").findPlaceByName("WaitingRoom").tokens == 3


def roomEmpty():
    return findPetriNetByName("Hospital").findPlaceByName("WaitingRoom").tokens == 0


loadHospital.runSimulations(5, 80, 4, 1337, 'hr', [
    ('Waiting room is full', .05, roomFull),
    ('Waiting room is empty', .05, roomEmpty)])
