import sys
sys.path.append('../pyHand/pyHand_API')
import pyHand_api as hand
import time as t
FINGER1 = 11	# Puck ID for F1
FINGER2 = 12	# Puck ID for F2
FINGER3 = 13	# Puck ID for F3
#from HandFunc import Hand,HandSensor,SensorShow

hand.initialize()
hand.init_hand()
while True:
    strain= hand.get_strain(FINGER1)
    print(strain)
    t.sleep(1)