from main.PetriNet import *

placeTokenMult = PetriNet('placeTokenMult')

Place1 = Place('Place1', placeTokenMult, 21)

Trans = ImmediateTransition('Trans', placeTokenMult)

Place2 = Place('Place2', placeTokenMult)

PlaceAux = Place('PlaceAux', placeTokenMult)

PlaceAux2 = Place('PlaceAux2', placeTokenMult, 1)

AuxOut = OutputArc('AuxOut', placeTokenMult, Trans, PlaceAux)

Place3 = Place('Place3', placeTokenMult, 6)

Place4 = Place('Place4', placeTokenMult)

Trans2 = ImmediateTransition('Trans2', placeTokenMult)

AuxOut2 = OutputArc('AuxOut2', placeTokenMult, Trans2, PlaceAux2)

AuxIn2 = InputArc('AuxIn2', placeTokenMult, PlaceAux2, Trans)

AuxIn = InputArc('AuxIn', placeTokenMult, PlaceAux, Trans2)

BaseIn = InputArc('BaseIn', placeTokenMult, Place3, Trans2)

BaseOut = OutputArc('BaseOut', placeTokenMult, Trans2, Place4)


def VaryMult():
    if(Place3.tokens > 0):
        return Place3.tokens
    else:
        return 1


VaryIn = InputArc('VaryIn', placeTokenMult, Place1, Trans, VaryMult)

Out1 = OutputArc('Out1', placeTokenMult, Trans, Place2)


placeTokenMult.runSimulation(10)
