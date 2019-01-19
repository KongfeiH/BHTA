import paramiko
import  time
from  sys import stdin as IN
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

#sensor=SensorShow()
T=[]
ISOK=True




  # c=time.time()
  # hand.CloseSpeedControl()
  # print time.time()-c
  # sensor.DataShow()
  # #sensor.ISContinue = False
  # csv = CSVRecord()
  # csv.Record("C:\Users\hekon\Desktop\oo", sensor.GetData())
  # print "Record Tactile Finished!"
  # Strain = [BT.get_strain(FINGER1), BT.get_strain(FINGER2), BT.get_strain(FINGER3), \
  #           BT.get_position(FINGER1), BT.get_position(FINGER2), BT.get_position(FINGER3),
  #           BT.get_position(SPREAD)]
  # csv.Record("C:\Users\hekon\Desktop\oo1", Strain)
  # print "Record Strain Finished!"
  # ISOK = False



ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    ssh.connect(hostname='192.168.149.102', port=22, username='robot', password='WAM')
except:
    print "connect failed"
    quit()


aa=ssh.invoke_shell()
aa.settimeout(9000)
#time.sleep(5)
aa.send("cd Eric_WorkSpace/libbarrett_examples/\n")
time.sleep(10)
print aa.recv(1000)

aa.send("./ex03_simple_move\n")
if True:#aa.recv(1000)=="./ex03_simple_move\n>>> The WAM needs to be zeroed. Please move it to its home position, then press [Enter].\n":
    aa.send("\n")

time.sleep(5)
print aa.recv(1000)

aa.send("j 0 -1.5 0 -0.6\n")
time.sleep(3)
print aa.recv(1000)
hand = Hand()
time.sleep(10)

sensor = SensorShow()
def ImgShow():
    sensor.DataShow()

def Action():
         hand.CloseSpeedControl()
         time.sleep(2)
         sensor.ISContinue=False
         T[2].start()
        # while  sensor.ISContinue:
          #   pass

def Record():
    csv=CSVRecord()
    csv.Record("C:\Users\hekon\Desktop\T",sensor.GetData())
    print "Record Tactile Finished!"
    Strain = [BT.get_strain(FINGER1), BT.get_strain(FINGER2), BT.get_strain(FINGER3), \
              BT.get_position(FINGER1),BT.get_position(FINGER2),BT.get_position(FINGER3),
              BT.get_position(SPREAD)]
    csv.Record("C:\Users\hekon\Desktop\T1",Strain)
    print "Record Strain Finished!"
    ISOK=False

def RECORDCVS():
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

RECORDCVS()
while sensor.ISContinue:
    pass
aa.send("h\n")
time.sleep(15)
print aa.recv(1000)

aa.send("i\n")
time.sleep(5)
print aa.recv(1000)
aa.send("q\n")
time.sleep(3)
print aa.recv(1000)
time.sleep(10)
ssh.close()


#def ImgShow():
#    sensor.DataShow()
#
#def Action():
#         hand.CloseSpeedControl()
#         time.sleep(3)
#         sensor.ISContinue=False
#         T[2].start()
#        # while  sensor.ISContinue:
#          #   pass
#
#def Record():
#    csv=CSVRecord()
#    csv.Record("C:\Users\hekon\Desktop\TEST",sensor.GetData())
#    print "Record Tactile Finished!"
#    Strain = [BT.get_strain(FINGER1), BT.get_strain(FINGER2), BT.get_strain(FINGER3), \
#              BT.get_position(FINGER1),BT.get_position(FINGER2),BT.get_position(FINGER3),
#              BT.get_position(SPREAD)]
#    csv.Record("C:\Users\hekon\Desktop\TEST1",Strain)
#    print "Record Strain Finished!"
#    ISOK=False
#    #exit()


#Thr = TH.Thread(target=ImgShow)
#T.append(Thr)
#T[0].setDaemon(True)
#Thr1 = TH.Thread(target=Action)
#T.append(Thr1)
#T[1].setDaemon(True)
#Thr2 = TH.Thread(target=Record)
#T.append(Thr2)
#T[2].setDaemon(True)
#T[0].start()
#T[1].start()


