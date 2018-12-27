# Ex07-ReadTactileData.py 
#
# Reading tactile data from the sensors is not a simple task. Rather than 
# generating a single CAN frame, as most of the gets do, reading the full
# tactile data yields five CAN frames. 
# 
# More information found in CAN_Message_Format in the manuals folder of pyHand.
#
import sys
import time
sys.path.append('../pyHand/pyHand_API')
import pyHand_api as hand
from puck_properties_consts import (FINGER1, FINGER2, FINGER3, SPREAD, TACT,
                                    TACT_FULL, TACT_10)
PCAN_ERROR_OKAY = 0 # If there are no issues, this is the "error" value.

hand.initialize()
hand.init_hand()

# Let's start by defining a class to get the data for us, so that repeated
# tactile gets are not difficult.
class HandSensor:

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

# Now that we've completed the class definition, let's implement it.
sensor = HandSensor()

# Get tactile data from hand 100 times.
for i in range(100):
    #print data
    print sensor.finger1
    print sensor.finger2
    print sensor.finger3
    print sensor.spread
    print '\n'

    time.sleep(.33) # Sleep for a short time.

    # collect data
    sensor.get_full_tact()
