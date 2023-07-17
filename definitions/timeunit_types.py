# definitions/timeunit_types.py module for Petri Net Project
# contains enumeration for timeUnit setting of Timed Transition objects and Petri Net simulation
# contains function to calculate conversion ratio if Timed Transition's timeUnit parameter differs from Petri Net simulation's default timeUnit parameter

from enum import Enum


class TimeUnitType(Enum):
    '''
    Enumeration of valid Time Unit types.
    '''
    n_sec = "nanosecond"
    mic_sec = "microsecond"
    mil_sec = "millisecond"
    sec = "second"
    min = "minute"
    hr = "hour"
    d = "day"
    w = "week"


# list of valid (used) time units
timerank = ['n_sec', 'mic_sec', 'mil_sec', 'sec', 'min', 'hr', 'd', 'w']
# list of upward conversion rates between used time units
rate = [1000, 1000, 1000, 60, 60, 24, 7]


def getTimeMultiplier(simUnit, objUnit):
    '''
    Function to return multiplier conversion rate in case of non-unified time unit usage during simulation.
    '''
    mult = 1
    if (timerank.index(objUnit) == timerank.index(simUnit)):
        return mult
    elif (timerank.index(objUnit) < timerank.index(simUnit)):
        index1 = timerank.index(objUnit)
        index2 = timerank.index(simUnit)
        for numb in rate[index1:index2]:
            mult = mult * (1/numb)
        return mult

    elif (timerank.index(objUnit) > timerank.index(simUnit)):
        index1 = timerank.index(simUnit)
        index2 = timerank.index(objUnit)
        for numb in rate[index1:index2]:
            mult = mult * numb
        return mult
