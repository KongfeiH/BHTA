# Ex05-GetBasicProperties.py
# 
# Use the get_property function to do exactly that. The functionality is 
# straightforward, but I suppose that some of the subtleties can be confusing.
#
# Of all the aforementioned subtleties, there is one primary issue. The method
# get_property() does not work with group messages. This is a known bug, but 
# not high on the fix queue.

import sys
import time
import Ex05a as helper

sys.path.append('../pyHand/pyHand_API')
import pyHand_api as hand
from puck_properties_consts import (FINGER1, FINGER2, FINGER3, SPREAD, VERS, 
    ROLE, MODE, T, MT, V, MV, P, JP)
	# Listed above are the properties for which I will walk you through the 
    #'get' process. There are more properties, of course, but these are the 
	# most common and useful ones.

# As always, we mmust initialize the hand.
hand.initialize()
hand.init_hand()

# Rather than launching into lengthy explanations of things, I will instead 
# show you several examples, and allow the print statements to do the talking.
print "Firmware Versions"
print "Finger 1: ", hand.get_property(FINGER1, VERS)
print "Finger 2: ", hand.get_property(FINGER2, VERS)
print "Finger 3: ", hand.get_property(FINGER3, VERS)
print "Spread  : ", hand.get_property(SPREAD, VERS)

print "\nRaw Role Data"
f1 = hand.get_property(FINGER1, ROLE)
print "Finger 1: ", f1
f2 = hand.get_property(FINGER2, ROLE)
print "Finger 2: ", f2
f3 = hand.get_property(FINGER3, ROLE)
print "Finger 3: ", f3
sp = hand.get_property(SPREAD, ROLE)
print "Spread  : ", sp

print "\nParsed Role Data"
print "Finger 1: ", helper.parse_role(f1)
print "Finger 2: ", helper.parse_role(f2)
print "Finger 3: ", helper.parse_role(f3)
print "Spread  : ", helper.parse_role(sp)

print "\nMotor Modes"
f1 = hand.get_property(FINGER1, MODE)
print "Finger 1: ", f1
f2 = hand.get_property(FINGER2, MODE)
print "Finger 2: ", f2
f3 = hand.get_property(FINGER3, MODE)
print "Finger 3: ", f3
sp = hand.get_property(SPREAD, MODE)
print "Spread  : ", sp

print "\nParsed Mode Data"
print "Finger 1: ", helper.parse_mode(f1)
print "Finger 2: ", helper.parse_mode(f2)
print "Finger 3: ", helper.parse_mode(f3)
print "Spread  : ", helper.parse_mode(sp)

print "\nTorque | Velocity"
print "F1: ", hand.get_property(FINGER1, T), "|", hand.get_property(FINGER1, V)
print "F2: ", hand.get_property(FINGER2, T), "|", hand.get_property(FINGER2, V)
print "F3: ", hand.get_property(FINGER3, T), "|", hand.get_property(FINGER3, V)
print "Sp: ", hand.get_property(SPREAD, T), "|", hand.get_property(SPREAD, V)

print "\nMax Torque | Max Velocity"
print "F1: ", hand.get_property(FINGER1, MT), "|", hand.get_property(FINGER1, MV)
print "F2: ", hand.get_property(FINGER2, MT), "|", hand.get_property(FINGER2, MV)
print "F3: ", hand.get_property(FINGER3, MT), "|", hand.get_property(FINGER3, MV)
print "Sp: ", hand.get_property(SPREAD, MT), "|", hand.get_property(SPREAD, MV)

# NOTE: Although the above is fairly straightforward and self-explanatory, the
# position data is not as nice. It's packed in such a manner that the general 
# 'get_property' method fails, so its own 'get_position' method must be used.
print "\nPosition Data"
print "F1: ", hand.get_position(FINGER1)
print "F2: ", hand.get_position(FINGER2)
print "F3: ", hand.get_position(FINGER3)
print "Sp: ", hand.get_position(SPREAD)

print "\nPacked Position Data"
print "F1: ", hand.get_packed_position(FINGER1)
print "F2: ", hand.get_packed_position(FINGER2)
print "F3: ", hand.get_packed_position(FINGER3)
print "Sp: ", hand.get_packed_position(SPREAD)

hand.set_property(0x405, MODE, 0)