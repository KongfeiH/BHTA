# Ex02-OpenCloseHandSimple.py
# 
# A simple program to open and close the hand in the easiest way possible.

# Imports
import sys
sys.path.append('../pyHand/pyHand_API')
import pyHand_api as hand
import time

# Initialize hand
hand.initialize()
hand.init_hand()

# Open and close fingers (grasp), then open and close spread.
hand.close_grasp()
hand.open_grasp()
hand.close_spread()
hand.open_spread()

# Note that the hand may collide with itself if you do not wait for the grasp 
# to finish moving before moving the spread. That is taken care of in the API,
# but as you learn finer techniques for controlling the  hand, this may become 
# more of a problem.
# For the more advanced user, this 'move' command uses the CMD property's
# OPEN and CLOSE routines.
