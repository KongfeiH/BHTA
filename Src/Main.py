import sys
sys.path.append('../HandAssembly')
sys.path.append('../Helper/DataToCSV')
sys.path.append('../pyHand/pyHand_API')
# This file may be run straight from this folder, but the above path can be
# modified to point to the API file.
import pyHand_api as BT
import time
import os
import matplotlib.pyplot as plt
import matplotlib as cm
from HandFunc import Hand,HandSensor,SensorShow
from DataToCSV import CSVRecord
from mpl_toolkits.mplot3d  import Axes3D
import numpy as np
import threading as TH
FINGER1 = 11	# Puck ID for F1
FINGER2 = 12	# Puck ID for F2
FINGER3 = 13	# Puck ID for F3
SPREAD  = 14	# Puck ID for SP
HAND_GROUP = 0x405 	# Refers to all motors that respond to group ID 5.
hand = Hand()
sensor=SensorShow()
T=[]
ISOK=True
# Now that we've completed the class definition, let's implement it.
#self.Strain=[hand.get_strain(FINGER1),hand.get_strain(FINGER2),hand.get_strain(FINGER3),\
  #                    hand.get_position(FINGER1),hand.get_position(FINGER2),hand.get_position(FINGER3)]
def ImgShow():
    sensor.DataShow()

def Action():
         hand.CloseSpeedControl()
         time.sleep(3)
         sensor.ISContinue=False
         T[2].start()
        # while  sensor.ISContinue:
          #   pass

def Record():
    csv=CSVRecord()
    csv.Record("C:\Users\hekon\Desktop\TEST",sensor.GetData())
    print "Record Tactile Finished!"
    Strain = [BT.get_strain(FINGER1), BT.get_strain(FINGER2), BT.get_strain(FINGER3), \
              BT.get_position(FINGER1),BT.get_position(FINGER2),BT.get_position(FINGER3),
              BT.get_position(SPREAD)]
    csv.Record("C:\Users\hekon\Desktop\TEST1",Strain)
    print "Record Strain Finished!"
    ISOK=False
    #exit()


Thr = TH.Thread(target=ImgShow)
T.append(Thr)
T[0].setDaemon(True)
Thr1 = TH.Thread(target=Action)
T.append(Thr1)
T[1].setDaemon(True)
Thr2 = TH.Thread(target=Record)
T.append(Thr2)
T[2].setDaemon(True)
T[0].start()
T[1].start()

while ISOK:
    pass







