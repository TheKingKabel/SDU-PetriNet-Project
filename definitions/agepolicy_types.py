# definitions/agepolicy_types.py module for Petri Net Project
# contains enumeration for agePolicy setting of Timed Transition objects

from enum import Enum


class AgePolicyType(Enum):
    '''
    Enumeration of valid Age Policy types.
    '''
    R_ENABLE = "Race Enable"
    R_AGE = "Race Age"
