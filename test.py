from PetriNet import *
import random
import scipy as sp

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

dsa = TimedTransition('asd', asd, 'NORM', 'race')
