# definitions/agepolicy_types.py module for Petri Net Project
# contains enumeration for agepolicy setting of Timed Transition objects

from enum import Enum


class AgePolicyType(Enum):
    R_ENABLE = "Race Enable"
    R_AGE = "Race Age"
