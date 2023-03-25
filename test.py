from PetriNet import *
import random
from simulation import runSimulation

import scipy as sp
import numpy as np

test = PetriNet("test")

# testPlace = Place("test1", test, 5)

# testTrans = TimedTransition("test1", test, "normal", "race")

# InputArc("test1", test, testPlace, testTrans, testPlace.tokens)

# testPlace.setTokens(10)

# # test.describe()

# list1 = [1, 2, 3, 4, 5]
# random.shuffle(list1)
# print(sp.__version__)

# testTimed = TimedTransition(asd, test, 'CAU', 'race')

asd = PetriNet('asdasd')

dsa = TimedTransition('asd', asd, 'NORM', 0, 1)

psad = TimedTransition('asdasdsa', asd, 'NORM', 1, 2.4)

# runSimulation(asd, 5)

scipy_num = sp.stats.norm.rvs(0.0, 1.0)
print(scipy_num)
print(scipy_num + 0.0)

numpy_num = np.random.normal(0.0, 1.0)
print(numpy_num)
print(numpy_num + 0.0)
