from main.PetriNet import *

raceage = PetriNet("RaceAge")

Start1 = Place("Start1", raceage, 1)
Start2 = Place("Start2", raceage, 1)
Hold = Place("Hold", raceage)
End = Place("End", raceage)

Delayed = TimedTransition("Delayed", raceage, 'NORM',
                          10.0, 2.0, agePolicy='R_AGE')
Early = TimedTransition("Early", raceage, 'NORM', 3.0, 1.5)
Later = TimedTransition("Later", raceage, 'NORM', 6.5, 2.3)

Start1 = InputArc("Start1", raceage, Start1, Early)
Start2 = InputArc("Start2", raceage, Start2, Delayed)
ToHold = OutputArc("ToHold", raceage, Early, Hold)
Inhib = InhibArc("Inhib", raceage, Hold, Delayed)
ToLater = InputArc("ToLater", raceage, Hold, Later)
End1 = OutputArc("End1", raceage, Later, End)
End2 = OutputArc("End2", raceage, Delayed, End)

raceage.runSimulation(35)
