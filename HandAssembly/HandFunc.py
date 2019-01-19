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
from puck_properties_consts import (FINGER1, FINGER2, FINGER3, SPREAD, TACT,
                                    TACT_FULL, TACT_10)
PCAN_ERROR_OKAY = 0 # If there are no issues, this is the "error" value.
import time
import matplotlib.pyplot as plt
import matplotlib as cm
import numpy as np


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



MODE_VEL = 4
V = 44
TSTOP = 78




class Hand():
    def __init__(self):

        # Firstly, communications with the CAN must be initialized. Otherwise, no
        # commands will be sent or received.
        # This next command tells each finger to perform the hand initialization (HI)
        # process. This involves the fingers moving to the home positions, so make sure
        # to clear the area so that the hand is not obstructed.
        hand.initialize()
        hand.init_hand()

      #  print "OK"

    def OpenACloseDemo(self):
        hand.close_grasp()
        hand.open_grasp()
        hand.close_spread()
        hand.open_spread()
        return True

    def Close(self):
        # Close fingers by setting the Move target to fully closed.
        hand.set_property(SPREAD, MODE, MODE_IDLE)
        #hand.close_grasp()
        hand.set_property(FINGER1, M, MAX_ENC)
        hand.set_property(FINGER2, M, MAX_ENC)
        hand.set_property(FINGER3, M, MAX_ENC)
        # ... and don't forget to stop the spread quickly.
        hand.set_property(SPREAD, MODE, MODE_IDLE)
        return True
    def CloseSpeedControl(self):
        hand.set_property(SPREAD, V, 0)
        hand.set_property(FINGER1, V, 80)  # Units are encoder counts per second
        hand.set_property(FINGER2, V, 80)
        hand.set_property(FINGER3, V, 80)

        # Set the timestop property to wait an arbitrarily long amount of time.
        # In general, the argument to TSTOP is amount of time in miliseconds that the
        # hand will wait to finish moving. Setting TSTOP to 0, however, makes that
        # tolerance level infinite. By default, the fingers wait 50 ms, and the spread
        # waits up to 150 ms.
        hand.set_property(HAND_GROUP, TSTOP, 0)

        # The hand must now go into velocity mode to move.
        hand.set_property(HAND_GROUP, MODE, MODE_VEL)
        time.sleep(3)
        hand.set_property(HAND_GROUP, MODE, MODE_IDLE)

        # Using the exact same process, we close the fingers.
    #    hand.set_property(FINGER1, V, -200)
    #    hand.set_property(FINGER2, V, -200)
    #    hand.set_property(FINGER3, V, -200)
    #    hand.set_property(HAND_GROUP, MODE, MODE_VEL)
    #    time.sleep(1.5)
    #    hand.set_property(HAND_GROUP, MODE, MODE_IDLE)

    ##   # Now, we open and close the spread.
    #   hand.set_property(HAND_GROUP, V, 0)
    #   hand.set_property(SPREAD, V, 60)
    #   hand.set_property(SPREAD, MODE, MODE_VEL)
    #   time.sleep(1.5)
    #   hand.set_property(SPREAD, MODE, MODE_IDLE)
    #   hand.set_property(SPREAD, V, -60)
    #   hand.set_property(SPREAD, MODE, MODE_VEL)
    #   time.sleep(1.5)

        # Because having an infinite timestop can wear out the hand, we now return them
        # to their default values.
        hand.set_property(HAND_GROUP, TSTOP, 50)
        hand.set_property(SPREAD, TSTOP, 150)
        return True
    def Test(self):
        hand.set_property(HAND_GROUP, M, MIN_ENC)
        hand.set_property(SPREAD, MODE, MODE_IDLE)
        time.sleep(1.5)

        # Closing spread
        hand.set_property(SPREAD, M, MAX_ENC)
        time.sleep(1.5)
        hand.set_property(HAND_GROUP, MODE, MODE_IDLE)
        time.sleep(1.5)
        hand.set_property(SPREAD, M, MIN_ENC)
        hand.set_property(SPREAD, MODE, MODE_IDLE)
        time.sleep(1.5)
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

#         print "OK"
    def ClosePositionControl(self):
        # Close fingers by setting the Move target to fully closed.
        hand.set_property(FINGER1, M, MAX_ENC)
        hand.set_property(FINGER2, M, MAX_ENC)
        hand.set_property(FINGER3, M, MAX_ENC)
        # ... and don't forget to stop the spread quickly.
        hand.set_property(SPREAD, MODE, MODE_IDLE)
        # Now we wait for the fingers to stop moving so that fingers and spread don't
        # run into one another.
        time.sleep(1.5)
        pass

class HandSensor(object):

    # The constructor for the sensor.
    def __init__(self):
        self.finger1 = []
        self.finger2 = []
        self.finger3 = []
        self.spread  = []
        # Populate these arrays by getting the full tactile data.
        self.get_full_tact()

    def get_full_tact(self):
        # Initialize the arrays by filling them with 24 values.
        self.finger1 = range(24)
        self.finger2 = range(24)
        self.finger3 = range(24)
        self.spread  = range(24)

        # Now we need to read all 20 CAN frames for the tactile data.
        # Five from each of the four joints.
        can_frames = []
        # From the previous example, we find that the message being sent to the
        # CAN is going to be the following.
        msg_out = [TACT + 0x80, 0, TACT_FULL, 0]

        hand.write_msg(FINGER1, msg_out)
        r = hand.read_msg()
        while r[0] == PCAN_ERROR_OKAY: # Check that the read is working.
            can_frames.append(r[1]) # Adding the message to our CAN frames.
            r = hand.read_msg() # Read the message back in.

        # Doing the same thing for the rest of the joints.
        hand.write_msg(FINGER2, msg_out)
        r = hand.read_msg()
        while r[0] == PCAN_ERROR_OKAY:
            can_frames.append(r[1])
            r = hand.read_msg()
        hand.write_msg(FINGER3, msg_out)
        r = hand.read_msg()
        while r[0] == PCAN_ERROR_OKAY:
            can_frames.append(r[1])
            r = hand.read_msg()
        hand.write_msg(SPREAD, msg_out)
        r = hand.read_msg()
        while r[0] == PCAN_ERROR_OKAY:
            can_frames.append(r[1])
            r = hand.read_msg()

        # Now we interpret these messages.
        # Each frame ID corresponds to the finger where the CAN frame is from.
        for frame in can_frames:
            if frame.ID == 0x569: # Full tact from finger 1
                self.interpret_full(self.finger1, frame)
            if frame.ID == 0x589: # Full tact from Finger 2
                self.interpret_full(self.finger2, frame)
            if frame.ID == 0x5A9: # Full tact From finger 3
                self.interpret_full(self.finger3, frame)
            if frame.ID == 0x5C9: # Full tact From spread
                self.interpret_full(self.spread, frame)

    def interpret_full(self, tact_array, frame):
        #Set up data to parse.
        data = frame.DATA

        # Starting index. The first half-byte tells the order of the data.
        index = int(data[0]/16) * 5

        # Get the array data and unpack it.
        tact_array[index + 0] = round(((data[0]<<8 & 0xF00) | data[1])/256.0, 2)
        tact_array[index + 1] = round((data[2]<<4 | data[3]>>4)/256.0, 2)
        tact_array[index + 2] = round(((data[3]<<8 & 0xF00) | data[4])/256.0, 2)
        tact_array[index + 3] = round((data[5]<<4 | data[6]>>4)/256.0, 2)
        if index != 20: # There are only 24 sensors per array.
            tact_array[index + 4] = round(((data[6]<<8 & 0xF00)| data[7])/256.0, 2)


class SensorShow(HandSensor):
    def __init__(self):
         super(SensorShow,self).__init__()
         self.sensorData = np.array(self.finger1+self.finger2+self.finger3+self.spread)
         #self.DataShow()

    def DataShow(self):
        fig = plt.figure()
        plt.ion()
        while True:
           # timeb=time.time()
            self.sensorData=np.vstack((self.sensorData,self.finger1+self.finger2+self.finger3+self.spread))

           # self.Show()
            time.sleep(0.036)
            self.get_full_tact()
         #   timee=time.time()
         #   print timee-timeb
    def Show(self):
        dataTest = np.array([self.finger1[0:3],
                             self.finger1[3:6],
                             self.finger1[6:9],
                             self.finger1[9:12],
                             self.finger1[12:15],
                             self.finger1[15:18],
                             self.finger1[18:21],
                             self.finger1[21:24]])
        dataTest1 = np.array([self.finger2[0:3],
                              self.finger2[3:6],
                              self.finger2[6:9],
                              self.finger2[9:12],
                              self.finger2[12:15],
                              self.finger2[15:18],
                              self.finger2[18:21],
                              self.finger2[21:24]])
        dataTest2 = np.array([self.finger3[0:3],
                              self.finger3[3:6],
                              self.finger3[6:9],
                              self.finger3[9:12],
                              self.finger3[12:15],
                              self.finger3[15:18],
                              self.finger3[18:21],
                              self.finger3[21:24]])

        x = self.spread[0:5]
        x.insert(0, 0)
        x.append(0)
        y = self.spread[19:24]
        y.insert(0, 0)
        y.append(0)
        dataTest3 = np.array([x,
                              self.spread[5:12],
                              self.spread[12:19],
                              y])
        # dataTest3.
        plt.clf()
        ax = fig.add_subplot(221)
        ax.imshow(dataTest)
        ax = fig.add_subplot(222)
        ax.imshow(dataTest1)
        ax = fig.add_subplot(223)
        ax.imshow(dataTest2)
        ax = fig.add_subplot(224)
        ax.imshow(dataTest3)
        plt.pause(0.09)

        plt.ioff()
    def GetData(self):
        return self.sensorData
    def DynamicData(self):
        dataTest=[]
        plt.ion()
        for i in range(10000):
           dataTest.append(self.finger1)
           plt.clf()
           plt.imshow(dataTest)
           plt.pause(0.33)
           plt.ioff()
           self.get_full_tact()

class VelocityMoveControl():
    def __init__(self):
        # Because fingers and spread may collide, we do not want the hand to move
        # spread at the same time as the fingers.
        hand.set_property(SPREAD, V, 0)
        hand.set_property(FINGER1, V, 200)  # Units are encoder counts per second
        hand.set_property(FINGER2, V, 200)
        hand.set_property(FINGER3, V, 200)

        # Set the timestop property to wait an arbitrarily long amount of time.
        # In general, the argument to TSTOP is amount of time in miliseconds that the
        # hand will wait to finish moving. Setting TSTOP to 0, however, makes that
        # tolerance level infinite. By default, the fingers wait 50 ms, and the spread
        # waits up to 150 ms.
        hand.set_property(HAND_GROUP, TSTOP, 0)

        # The hand must now go into velocity mode to move.
        hand.set_property(HAND_GROUP, MODE, MODE_VEL)
        time.sleep(1.5)
        hand.set_property(HAND_GROUP, MODE, MODE_IDLE)

        # Using the exact same process, we close the fingers.
        hand.set_property(FINGER1, V, -200)
        hand.set_property(FINGER2, V, -200)
        hand.set_property(FINGER3, V, -200)
        hand.set_property(HAND_GROUP, MODE, MODE_VEL)
        time.sleep(1.5)
        hand.set_property(HAND_GROUP, MODE, MODE_IDLE)

        # Now, we open and close the spread.
        hand.set_property(HAND_GROUP, V, 0)
        hand.set_property(SPREAD, V, 60)
        hand.set_property(SPREAD, MODE, MODE_VEL)
        time.sleep(1.5)
        hand.set_property(SPREAD, MODE, MODE_IDLE)
        hand.set_property(SPREAD, V, -60)
        hand.set_property(SPREAD, MODE, MODE_VEL)
        time.sleep(1.5)

        # Because having an infinite timestop can wear out the hand, we now return them
        # to their default values.
        hand.set_property(HAND_GROUP, TSTOP, 50)
        hand.set_property(SPREAD, TSTOP, 150)
