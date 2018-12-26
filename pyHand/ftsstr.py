# ftsstr.py
#
# Defines an object to hold FTS data

import pyHand_API.pyHand_api as bt
PCAN_ERROR_OK = 0           #PCAN Error Value for no error

#============================FTS=CLASS=DEFINITION=============================#
class ftsstr:
    '''
    Holds all of the force-torque data.

        @cvar forceX: Float representing force in the x-direction.
        @cvar forceY: Float representing force in the y-direction.
        @cvar forceZ: Float representing force in the z-direction.
        @cvar torqueX: Float representing torque in the x-direction.
        @cvar torqueY: Float representing torque in the y-direction.
        @cvar torqueZ: Float representing torque in the z-direction.
        @cvar error_byte: Byte representing if the sensor has errored.
    '''

    def update(self):
        '''
        Collects and interprets force-torque data
        '''
        msgs = self.read_ftdata()
        data = msgs[0][1].DATA
        
        val = data[1] * 0x100 + data[0] #raw data value
        val = val if val < 0x8000 else bt.twoscomp(val, 16)
        self.forceX = round(val/256.0, 2)

        val = data[3] * 0x100 + data[2]
        val = val if val < 0x8000 else bt.twoscomp(val, 16)
        self.forceY = round(val/256.0, 2)
        
        val = data[5] + 0x100 + data[4] - 0x100
        val = val if val < 0x8000 else bt.twoscomp(val, 16)
        self.forceZ = round(val/256.0, 2)
        
        data = msgs[1][1].DATA
        
        val = data[1] * 0x100 + data[0]
        val = val if val < 0x8000 else bt.twoscomp(val, 16)
        self.torqueX = round(val/4096.0, 3)
        
        val = data[3] * 0x100 + data[2]
        val = val if val < 0x8000 else bt.twoscomp(val, 16)
        self.torqueY = round(val/4096.0, 3)
        
        val = data[5] + 0x100 + data[4] - 0x100
        val = val if val < 0x8000 else bt.twoscomp(val, 16)
        self.torqueZ = round(val/4096.0, 3)

        self.error_byte = 0
        if msgs[1][1].LEN > 6:
            self.error_byte = msgs[1][1].DATA[6]
        
        # print "FT DATA"
        # print self.forceX, self.forceY, self.forceZ
        # print self.torqueX, self.torqueY, self.torqueZ

    def tare(self):
        '''
        Tare the FTS sensor.
        '''
        bt.set_property(bt.FTS, bt.FTS_FT, 0)
        self.error_byte = 0

    def __init__(self):
        self.forceX = float()
        self.forceY = float()
        self.forceZ = float()
        self.torqueX = float()
        self.torqueY = float()
        self.torqueZ = float()
        self.error_byte = 0
        try:
            self.initialize_fts()
        except:
            pass

    def initialize_fts(self):
        '''
        Wake pucks and tare sensor.
        '''
        bt.set_property(bt.FTS, bt.STAT, 2)
        bt.set_property(bt.FTS, bt.FTS_FT, 0)

    def read_ftdata(self):
        '''
        The force-torque sensor returns two CAN frames. This method returns 
        both of those CAN frames in a tuple.

            @rtype: ((TPCANStatus, TPCANMsg, TPCANTimestamp), 
            (TPCANStatus, TPCANMsg, TPCANTimestamp))
            
            @return: Both CAN Frames from the FTS in a tuple.
        '''
        bt.can_reset()
        err = bt.write_msg(bt.FTS, [bt.FTS_FT])
        if err==PCAN_ERROR_OK:
            msg1 = bt.read_msg()
            while msg1[1].ID == 0:
                if msg1[0] != PCAN_ERROR_OK:
                    raise Exception("Force read failed. TPCANStatus("+hex(msg1[0])+")")
                msg1 = bt.read_msg()
            msg2 = bt.read_msg()
            while msg2[1].ID == 0:
                if msg1[0] != PCAN_ERROR_OK:
                    raise Exception("Torque read failed. TPCANStatus("+hex(msg2[0])+")")
                msg2 = bt.read_msg()
        else:
            raise Exception("write_msg failed: TPCANStatus("+hex(err)+")")
        # print "\nMsgIDs: ", hex(msg1[1].ID), hex(msg2[1].ID)
        # print "Raw Data: "
        # s = "msg1: "
        # for p in msg1[1].DATA:
        #     s += " "+hex(p)
        # print s
        # s = "msg2: "
        # for p in msg2[1].DATA:
        #     s += " "+hex(p)
        # print s
        return (msg1, msg2)
