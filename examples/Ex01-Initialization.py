# Ex01-Initialize.py
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

# Firstly, communications with the CAN must be initialized. Otherwise, no
# commands will be sent or received.
hand.initialize()

# This next command tells each finger to perform the hand initialization (HI)
# process. This involves the fingers moving to the home positions, so make sure
# to clear the area so that the hand is not obstructed.
hand.init_hand()

# The hand is now initialized. Note that there is a small hum from the spread,
# since it is no longer idling, but instead trying to hold its position.