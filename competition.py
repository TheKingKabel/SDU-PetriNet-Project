from main.PetriNet import *

# a simple PN consisting of mainly competing Immediate Transitions
# PN starts with a single StartP Place holding 1000 tokens
# the competing Immediate Transitions have different set probabilities of firing
# check logs to verify firings are consistent with set probability!


competition = PetriNet("Competition")

StartP = Place('StartP', competition, 1000)

TWait1 = ImmediateTransition("TWait1", competition, None, 0.25)
TWait2 = ImmediateTransition("TWait2", competition, None, 0.25)
TWait3 = ImmediateTransition("TWait3", competition, None, 0.50)

Inter1 = InputArc("Inter1", competition, StartP, TWait1)
Inter2 = InputArc("Inter2", competition, StartP, TWait2)
Inter3 = InputArc("Inter3", competition, StartP, TWait3)

InterPlace1 = Place("InterPlace1", competition)
InterPlace2 = Place("InterPlace2", competition)

Inter21 = OutputArc('Inter21', competition, TWait1, InterPlace1)
Inter22 = OutputArc('Inter22', competition, TWait2, InterPlace1)
Inter23 = OutputArc('Inter23', competition, TWait3, InterPlace2)

TWait21 = ImmediateTransition("TWait21", competition, None, 0.50)
TWait22 = ImmediateTransition("TWait22", competition, None, 0.50)
TWait23 = ImmediateTransition("TWait23", competition, None, 0.50)
TWait24 = ImmediateTransition("TWait24", competition, None, 0.50)

Inter31 = InputArc("Inter31", competition, InterPlace1, TWait21)
Inter32 = InputArc("Inter32", competition, InterPlace1, TWait22)
Inter33 = InputArc("Inter33", competition, InterPlace2, TWait23)
Inter34 = InputArc("Inter34", competition, InterPlace2, TWait24)

Final = Place('Final', competition)

Inter41 = OutputArc('Inter41', competition, TWait21, Final)
Inter42 = OutputArc('Inter42', competition, TWait22, Final)
Inter43 = OutputArc('Inter43', competition, TWait23, Final)
Inter44 = OutputArc('Inter44', competition, TWait24, Final)

# Pn only has Immediate Transitions, simLength is redundant: all events are executed at time 0.0, then clock is advanced to 123 seconds
competition.runSimulations(10, 123, 0)
