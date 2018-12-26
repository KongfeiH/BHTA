#
#
# This is one of the simplest programs possible to run the Barrett Hand.
#
# Before running this program, power on the Hand and connect it to the host
# PC.
#

import sys
sys.path.append('../pyHand/pyHand_API')
# This file may be run straight from this folder, but the above path can be
# modified to point to the API file.
import pyHand_api as hand
import time



# Set up constants. A complete list of property ids can be found online at
# http://web.barrett.com/support/Puck_Documentation/PuckProperties-r200.pdf
MODE = 8
MODE_IDLE= 0
M = 58			# Position move command

MIN_ENC = 0 		# The closed position for each motor.
MAX_ENC = 195000	# The open position for each motor.

FINGER1 = 11	# Puck ID for F1
FINGER2 = 12	# Puck ID for F2
FINGER3 = 13	# Puck ID for F3
SPREAD  = 14	# Puck ID for SP
HAND_GROUP = 0x405 	# Refers to all motors that respond to group ID 5.
class Hand():
    def __init__(self):

        # Firstly, communications with the CAN must be initialized. Otherwise, no
        # commands will be sent or received.
        # This next command tells each finger to perform the hand initialization (HI)
        # process. This involves the fingers moving to the home positions, so make sure
        # to clear the area so that the hand is not obstructed.
        hand.initialize()
        hand.init_hand()
        print "ok"

    def OpenACloseDemo(self):
        hand.close_grasp()
        hand.open_grasp()
        hand.close_spread()
        hand.open_spread()
        return True
    def PositionTest(self):

         # Close fingers by setting the Move target to fully closed.
         hand.set_property(HAND_GROUP, M, MAX_ENC)
         # ... and don't forget to stop the spread quickly.
         hand.set_property(SPREAD, MODE, MODE_IDLE)
         # Now we wait for the fingers to stop moving so that fingers and spread don't
         # run into one another.
         time.sleep(1.5)

         # Opening the fingers now.
         hand.set_property(HAND_GROUP, M, MIN_ENC)
         hand.set_property(SPREAD, MODE, MODE_IDLE)
         time.sleep(1.5)

         # Closing spread
         hand.set_property(SPREAD, M, MAX_ENC)
         time.sleep(1.5)

         # Open spread
         hand.set_property(SPREAD, M, MIN_ENC)
         time.sleep(1.5)

         hand.set_property(HAND_GROUP, MODE, MODE_IDLE)

         print "ok"
