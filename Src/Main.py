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



















# Get tactile data from hand 100 times.
#for i in range(100):
#    #print data
#    print str(sensor.finger1)
#  #  sys.stdout.write(str(sensor.finger2)+"\n")
#  #  sys.stdout.write(str(sensor.finger3)+"\n")
#  #  sys.stdout.write(str(sensor.spread)+"\n")
#    sys.stdout.flush()
#    time.sleep(.33) # Sleep for a short time.
#
#    # collect data
#    sensor.get_full_tact()


#dataTest=[]
#z=np.array(dataTest)
#
#plt.ion()
#for i in range(10000):
#
#    dataTest.append(sensor.finger1)
#    z = np.array(dataTest)
#    size = z.shape
#    print size
#    x = np.arange(0,size[0],1)
#    y = np.arange(0,size[1],1)
#    x,y=np.meshgrid(x,y)
#    plt.clf()
#    #plt.plot(dataTest)
#    ax.plot_surface(x,y,z)
#
#    plt.pause(0.1)
#  #  time.sleep(.33)
#    plt.ioff()
#    sensor.get_full_tact()



#dataTest=[]
#
#
#plt.ion()
#for i in range(10000):
#
#    dataTest.append(sensor.finger1)
#
#
#    plt.clf()
#
#    plt.imshow(dataTest)
#
#    plt.pause(0.33)
#  #  time.sleep(.33)
#    plt.ioff()
#    sensor.get_full_tact()#