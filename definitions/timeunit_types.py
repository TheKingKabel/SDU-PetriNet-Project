# definitions/timeunit_types.py module for Petri Net Project
# contains enumeration for timeunit setting of Timed Transition objects and Petri Net simulation
# contains function to calculate conversion ratio if Timed Transition's timeunit parameter differs from Petri Net simulation's default timeunit parameter

from enum import Enum


class TimeUnitType(Enum):
    n_sec = "nanosecond"
    mic_sec = "microsecond"
    mil_sec = "millisecond"
    sec = "second"
    min = "minute"
    hr = "hour"
    d = "day"
    w = "week"


timerank = ['n_sec', 'mic_sec', 'mil_sec', 'sec', 'min', 'hr', 'd', 'w']
rate = [1000, 1000, 1000, 60, 60, 24, 7]


def getTimeMultiplier(simUnit, objUnit):
    mult = 1
    if(timerank.index(objUnit) == timerank.index(simUnit)):
        return mult
    elif(timerank.index(objUnit) < timerank.index(simUnit)):
        index1 = timerank.index(objUnit)
        index2 = timerank.index(simUnit)
        for numb in rate[index1:index2]:
            mult = mult * (1/numb)
        return mult

    elif(timerank.index(objUnit) > timerank.index(simUnit)):
        index1 = timerank.index(simUnit)
        index2 = timerank.index(objUnit)
        for numb in rate[index1:index2]:
            mult = mult * numb
        return mult
