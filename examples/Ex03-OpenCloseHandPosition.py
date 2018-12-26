# Ex03-OpenCloseHandPosition.py
# 
# A simple program to open and close the hand using position controls.
#

# Imports
import sys
sys.path.append('../pyHand/pyHand_API')
import pyHand_api as hand
import time

# Initialize hand
hand.initialize()
hand.init_hand()

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
# Group ID 5 specifically references the hand motors.
# More about that can be found at the Barrett Support Site:
# http://web.barrett.com/support/Puck_Documentation/CAN_Message_Format.pdf
# Skip to page 2 for details how group IDs work.

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
