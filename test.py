from components.place import *
from main import *

print('1 item')

Place('start', True, 3, 5, 3)

getPlaces()

print('2 item')

Place('second')

getPlaces()

print('3 item + throw error')

Place('problem')
#Place('problem')

getPlaces()

print('3 item + changed values')

setName('second', 'second_changed')
setStart('start', False)
setTokens('problem', 100)
setTotalTokens('problem', 200)
setMaxTokens('problem', 150)

getPlaces()

print('should throw error')

#setStart('second', True) error

getPlaces()


