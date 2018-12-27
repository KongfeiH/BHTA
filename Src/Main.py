import sys
sys.path.append('../HandAssembly')
import time
import os
import matplotlib.pyplot as plt
import matplotlib as cm
from HandFunc import Hand,HandSensor,SensorShow
from mpl_toolkits.mplot3d  import Axes3D
import numpy as np
import threading as TH
hand = Hand()
#
# Now that we've completed the class definition, let's implement it.

def ImgShow():
    x=SensorShow()
    x.DataShow()

def Action():
    hand.Close()
    time.sleep(1)



T=[]
#showData = SensorShow()

Thr = TH.Thread(target=ImgShow)
T.append(Thr)
Thr1 = TH.Thread(target=Action)
T.append(Thr1)
T[0].start()
T[1].start()

while True:
    A=1







