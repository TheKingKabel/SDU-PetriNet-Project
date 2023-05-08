from main.PetriNet import *

# a simple PN showing the usability of memory policies
# 1-1 tokens start in Start1 and Start2 Places
# both are removed by a respective Timed Transitions; however one is slightly earlier (Early) than the other (Delayed)
# the one event firing earlier places a token in a Hold Place which has an Inhibitor Arc targeting the slightly later Timed Transition (Delayed)
# this puts Delayed on hold (...unless it was lucky enough to fire BEFORE Early fired)
# the Delayed Timed Transitions has race age memory policy, therefore it will remember the passing of time whilst being disabled
# after some time Later Timed Transition will fire, removing the token from Hold, thereby the Inhibitor Arc disabling Delayed has no longer an effect
# now Delayed is also enabled to fire, placing the token from Start2 to Finish (...unless it hasn't reached its original firing time by the time Later fires)

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

raceage.runSimulations(10, 35)
