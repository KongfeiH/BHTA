# Ex04-OpenCloseHandVelocity.py
# 
# A program to open and close the hand using the more advanced technique of 
# velocity controls.
#

# Imports
import sys
sys.path.append('../pyHand/pyHand_API')
import pyHand_api as hand
import time

# Set up constants, as in the last file.
MODE = 8
MODE_IDLE= 0
MODE_VEL = 4
V = 44
TSTOP = 78

FINGER1 = 11
FINGER2 = 12
FINGER3 = 13
SPREAD  = 14
HAND_GROUP = 0x405

# Initialize hand
hand.initialize()
hand.init_hand()

# Because fingers and spread may collide, we do not want the hand to move 
# spread at the same time as the fingers.
hand.set_property(SPREAD,  V, 0)
hand.set_property(FINGER1, V, 200) # Units are encoder counts per second 
hand.set_property(FINGER2, V, 200)
hand.set_property(FINGER3, V, 200)

# Set the timestop property to wait an arbitrarily long amount of time.
# In general, the argument to TSTOP is amount of time in miliseconds that the 
# hand will wait to finish moving. Setting TSTOP to 0, however, makes that 
# tolerance level infinite. By default, the fingers wait 50 ms, and the spread
# waits up to 150 ms.
hand.set_property(HAND_GROUP, TSTOP, 0)

# The hand must now go into velocity mode to move.
hand.set_property(HAND_GROUP, MODE, MODE_VEL)
time.sleep(1.5)
hand.set_property(HAND_GROUP, MODE, MODE_IDLE)

# Using the exact same process, we close the fingers.
hand.set_property(FINGER1, V, -200)
hand.set_property(FINGER2, V, -200)
hand.set_property(FINGER3, V, -200)
hand.set_property(HAND_GROUP, MODE, MODE_VEL)
time.sleep(1.5)
hand.set_property(HAND_GROUP, MODE, MODE_IDLE)

# Now, we open and close the spread.
hand.set_property(HAND_GROUP, V, 0)
hand.set_property(SPREAD, V, 60)
hand.set_property(SPREAD, MODE, MODE_VEL)
time.sleep(1.5)
hand.set_property(SPREAD, MODE, MODE_IDLE)
hand.set_property(SPREAD, V, -60)
hand.set_property(SPREAD, MODE, MODE_VEL)
time.sleep(1.5)

# Because having an infinite timestop can wear out the hand, we now return them
# to their default values.
hand.set_property(HAND_GROUP, TSTOP, 50)
hand.set_property(SPREAD, TSTOP, 150)
