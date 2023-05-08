from main.PetriNet import *

# a simple PN showing the capability of using current Place tokens for setting multiplicity of Arcs ( |A| )
# the main starting Place (Place1) has 21 tokens initially
# the secondary starting Place (Place3) has 6
# tokens are removed alternately (via Immediate Transitions; simLength is redundant here) from both starting places
# at each firing, 1 token is removed from Place3
# at each firing, the current token count of Place3 is removed from Place1
# (Reason: Sigma(6) = 21)

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

# correct syntax of defining dynamic multiplicities, callable functions returning integer values
# this way the function references can still be accessed from other modules, as well as PN temporary (in-simulation) values evaluated dynamically
# IMPORTANT: add checking with if...else, to NOT return 0; it CAN create errors if PN is not constructed properly


def VaryMult():
    if (Place3.tokens > 0):
        return Place3.tokens
    else:
        return 1


VaryIn = InputArc('VaryIn', placeTokenMult, Place1, Trans, VaryMult)

Out1 = OutputArc('Out1', placeTokenMult, Trans, Place2)


placeTokenMult.runSimulations(10, 10)
