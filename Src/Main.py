import sys
sys.path.append('../HandAssembly')
sys.path.append('../Helper/DataToCSV')
import time
import os
import matplotlib.pyplot as plt
import matplotlib as cm
from HandFunc import Hand,HandSensor,SensorShow
from DataToCSV import CSVRecord
from mpl_toolkits.mplot3d  import Axes3D
import numpy as np
import threading as TH

hand = Hand()
sensor=SensorShow()
T=[]
# Now that we've completed the class definition, let's implement it.

def ImgShow():
    sensor.DataShow()

def Action():
         hand.Close()
         time.sleep(2)
         T[2].start()

def Record():
    csv=CSVRecord.Record("C:\Users\hekon\Desktop\kk",sensor.GetData())



Thr = TH.Thread(target=Record)
T.append(Thr)
Thr1 = TH.Thread(target=Action)
T.append(Thr1)
Thr2 = TH.Thread(target=Action)
T.append(Thr2)
T[0].start()
T[1].start()

while True:
    pass







