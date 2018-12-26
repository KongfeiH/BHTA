#  pyHand_api.py
#  
#  ~~~~~~~~~~~~
#  
#  pyHand_api for Barrett Technology Hand Communications
#  
#  ~~~~~~~~~~~~
#  
#  ------------------------------------------------------------------
#  Authors : Chloe Eghtebas,
#            Brendan Ritter,
#            Pravina Samaratunga,
#            Jason Schwartz
#  
#  Last change: 08.08.2013
#
#  Language: Python 2.7
#  ------------------------------------------------------------------
# 
#  This version of pyHand is free software: you can redistribute it and/or
#  modify it under the terms of the GNU General Public License as published by the
#  Free Software Foundation.
#


from CAN_library import *
#  Copyright (C) 1999-2011  PEAK-System Technik GmbH, Darmstadt
#  more Info at http://www.peak-system.com 
#  Used under GNU General Public License.

from puck_properties_consts import*
from ctypes import *
import time

PCAN = PCANBasic()

#==========================CAN_STUFF=======================================

def check_error(connection,result,location_of_error):
    '''
    Checks error on the CAN Bus.

        @param connection: The connection on which the CAN is talking. For example, PCANBasic()
        @type connection: PCANBasic
        @param result: The number corresponding to the error returned.
        @type resulr: int
        @param location_of_error: A description of where the error occurred.
        @type location_of_error: str
    '''
    if result == PCAN_ERROR_OK:
        pass
    else:
        raise Exception("Error Number: " + hex(result) + " while attempting to " + str(location_of_error) + "\n" + connection.GetErrorText(result)[1])

def enum():
    '''
    Finds and returns all of the pucks that are attached to the bus.

        @rtype: Array[]
        @return: An array containing the pucks attached to the bus.
    '''
    pucks = []
    for i in range(32):
        try:
            get_property(i,1)
            pucks.append(i)
        except:
            pass
    return pucks

def can_reset():
    '''
    Resets the CAN connection.
    Note that this may cause a loss of data, but may also clear unwanted data. Utilize as needed.
    '''
    reset_result=PCAN.Reset(PCAN_USBBUS1)
    try:
        check_error(PCAN,reset_result,"reset")
    except:
        return False
    time.sleep(0.025)
    return True

def can_status():
    '''
    Returns the status of the CAN connection as specified in PCANBasic's GetStatus method.
    '''
    status_result=PCAN.GetStatus(PCAN_USBBUS1)
    time.sleep(0.025)
    return status_result

def can_init():
    '''
    Initializes the CAN connection. Note that this does not initialize the hand itself.
    '''
    global PCAN
    # initialize PCAN bus
    init_result=PCAN.Initialize(PCAN_USBBUS1, PCAN_BAUD_1M)
    check_error(PCAN,init_result,"initialize")
    time.sleep(0.025)

def can_uninit():
    '''
    Uninitializes the CAN connection. Rarely used.
    '''
    global PCAN
    uninit_result=PCAN.Uninitialize(PCAN_USBBUS1)
    check_error(PCAN,uninit_result,"uninitialize")
    
#============================INIT_STUFF==================================
    
def initialize():
    '''
    Wakes up pucks and initializes the CAN.
    This function must be implemented at the beginning of a program for this library to properly work.

        @rtype: ROLE
        @return: First finger's ROLE property if initialization is successful. Otherwise it returns False.
    '''
    try:
        can_init()
        #Reset Can bus
        can_reset()
        time.sleep(0.025)
        # wake up pucks by setting the STAT(5) property to READY(2)
        set_property(0x400, 5, 2)
        time.sleep(1)
        can_reset()
        return True
    except:
        return False

def init_hand():
    '''
    Initialize all pucks in the hand.

        @rtype: Boolean
        @return: Succesfully Initialized Hand?
    '''
    try:
        #write 13 to the command property (CMD-29) of each of the pucks.
        init_finger(FINGER1)
        init_finger(FINGER2)
        init_finger(FINGER3)
        time.sleep(3)
        init_finger(SPREAD)
        time.sleep(2)
        
        can_reset()
        get_property(FINGER1, ROLE)
        return True
    except:
        can_reset()
        return False

def init_finger(msgID):
    '''
    Sends a command to the puck to wake up the motor attatched to the puck.

        @param msgID: The id of the finger to initialize.
        @type msgID: int
    '''
    set_property(msgID, CMD, CMD_HI)

#============================SET_AND_GET_STUFF=========================

def read_msg():
    '''
    Read a general message from PCAN_USBBUS1
    Typically, msg[1] (where msg is the thing returned), contains the pertinent information.

        @rtype: (TPCANStatus, TPCANMsg, TPCANTimestamp)
        @return: A tuple containing the status, message, and timestamp.
    '''
    global PCAN
    return PCAN.Read(PCAN_USBBUS1)

def write_msg(msgID, data, delay=.015):
    '''
    Send a general message to PCAN_USBBUS1. This can be a get, set, or even garbage.

        @param msgID: The puck or group to which the message will be sent.
        @type msgID: int
        @param data: The array containing the data for the TPCANMsg.
        @type data: Array[]
        @param delay: The time delay to wait for the message to be written.
        @type delay: float
        @rtype: TPCANStatus
        @return: Status of the PCAN bus.
    '''
    global PCAN
    msg = TPCANMsg()
    msg.ID = msgID
    msg.LEN = len(data)
    msg.MSGTYPE = PCAN_MESSAGE_STANDARD
    for j in range(0, len(data)):
        msg.DATA[j] = data[j]
    stat = PCAN.Write(PCAN_USBBUS1, msg)
    check_error(PCAN,stat,"write")
    time.sleep(delay)
    return stat

def set_property(msgID, propID, value):
    '''
    Set property to a given value.

        @param msgID: The puck or group whose property will be set.
        @type msgID: int
        @param propID: The number corresponding to the property to be set.
        @type propID: int
        @param value: The value to which the property will be set.
        @type value: int
    '''
    is32bits = [48, 50, 52, 54, 56, 58, 66, 68, 74, 88, 96, 98]
    if propID in is32bits:
        set_32(msgID, propID, value)
    else:
        set_16(msgID, propID, value)
        
def set_32(msgID, propID, value):
    '''
    Set property to a given value for a 32 bit property.
    Avoid usage of this method. Use set_property instead.

        @param msgID: The puck or group whose property will be set.
        @type msgID: int
        @param propID: The number corresponding to the property to be set.
        @type propID: int
        @param value: The value to which the property will be set.
        @type value: int
    '''
    data = [0x80+propID, 0, value%0x100, int(value/0x100)%0x100, int(value/0x10000)%0x100, int(value/0x1000000)]
    write_msg(msgID, data)

def set_16(msgID, propID, value):
    '''
    Set property to a given value for a 16 bit property.
    Avoid usage of this method. Use set_property instead.
    
        @param msgID: The puck or group whose property will be set.
        @type msgID: int
        @param propID: The number corresponding to the property to be set.
        @type propID: int
        @param value: The value to which the property will be set.
        @type value: int
    '''
    data = [0x80+propID, 0, value%256, int(value/256)]
    write_msg(msgID, data)

# TODO: Allow a "GET" from a group.
def get_property(msgID, propID):
    '''
    Get property from pucks in msgID.

        @param msgID: The puck whose property will be read from.
        @type msgID: int
        @param propID: The property be read from.
        @type propID: int
        @rtype: int
        @return: The value held in the property.
    '''
    is32bits = [48, 50, 52, 54, 56, 58, 66, 68, 74, 88, 96, 98]
    if propID in is32bits:
        return get_32(msgID, propID)
    else:
        if propID == TACT:
            return get_tact(msgID)
        return get_16(msgID, propID)

def get_32(msgID, propID):
    '''
    Gets a 32 bit property. Please use get_property instead of this method where applicable.

        @param msgID: The puck whose property will be read from.
        @type msgID: int
        @param propID: The property be read from.
        @type propID: int
        @rtype: int
        @return: The value held in the property.
    '''
    global PCAN
    write_msg(msgID, [propID])
    time.sleep(0.05)
    read_result = PCAN.Read(PCAN_USBBUS1)
    check_error(PCAN, read_result[0], "read")
    data = read_result[1].DATA
    value = (0x1000000 * data[5]) + (0x0010000 * data[4]) + (0x0000100 * data[3]) + (0x0000001 * data[2])
    return value

def get_16(msgID, propID):
    '''
    Gets a 16 bit property. Please use get_property instead of this method where applicable.
    
        @param msgID: The puck whose property will be read from.
        @type msgID: int
        @param propID: The property be read from.
        @type propID: int
        @rtype: int
        @return: The value held in the property.
    '''
    global PCAN
    write_msg(msgID, [propID])
    time.sleep(0.05)
    read_result = PCAN.Read(PCAN_USBBUS1)
    check_error(PCAN, read_result[0], "read")
    data = read_result[1].DATA
    value =(0x0000100 * data[3]) + (0x0000001 * data[2])
    return value

def save_property(msgID, propID):
    '''
    Save a property.

        @param msgID: The puck or group to have its property saved.
        @type msgID: int
        @param propID: The property to be saved.
        @type propID: int
    '''
    set_property(msgID, SAVE, propID)

def load_property(msgID, propID):
    '''
    Load a property's value for puck's flash memory.

        @param msgID: The puck or group to have its property loaded.
        @type msgID: int
        @param propID: The property to be loaded.
        @type propID: int
    '''
    set_property(msgID, LOAD, propID)
    
def get_prop_quick(msgID,propID,speed):
    '''
    Gets a property timed at a certain rate.

        @param msgID: The puck or group to have its property gotten.
        @type msgID: int
        @param propID: The property to be saved.
        @type propID: int
        @param speed: The time delay for the get.
        @type speed: float
    '''
    global PCAN
    write_msg(msgID, [propID],speed)
    read_result=read_msg_resilient(msgID,propID)
    check_error(PCAN, read_result[0], "read")
    data = read_result[1].DATA
    value = (0x1000000 * data[5]) + (0x0010000 * data[4]) + (0x0000100 * data[3]) + (0x0000001 * data[2])
    return value

def read_msg_resilient(expect_puck,expect_prop,max_recurse=10,counter=0):
    '''
    Reads message given the puckID and the propertyID. 
    It will read as normal, until it gets some expected output from the puck.

        @param expect_puck: The puck to read from.
        @type expect_puck: int
        @param expect_prop: The property read from.
        @type expect_prop: int
        @param max_recurse: The most number of times to repeat the get.
        @type max_recurse: int
        @param counter: Used internally. Do not set.
        @type counter: int
        @rtype: int
        @return: The value held in the property of the given puck.
    '''
    counter+=1
    global PCAN
    response=PCAN.Read(PCAN_USBBUS1)
    received_prop=response[1].DATA[0]-128
    received_puck=(response[1].ID-1024)>>5
    
    if (received_prop==expect_prop) and (received_puck==expect_puck):
        return response
    else:
        print "a"
        if counter<max_recurse:
            return read_msg_resilient(expect_puck,expect_prop,counter=counter)
        else:
            raise Exception("Missed message")

def get_role(msgID):
    '''
    Read from ROLE property and return something that makes sense.
    Returns an array of holding the following data:

    [4-bit Product Identifier,
    Internal Thermistor,
    20 MHz (vs 32 MHz),
    Hall Motor Encoder,
    Enc Motor Encoder,
    Strain Gauge,
    IMU for Force-Torque Sensor,
    Optical Motor Encoder]

        @param msgID: The puck to get the ROLE from.
        @type msgID: int
        @rtype: Array[int,bool,bool,bool,bool,bool,bool,bool]
        @return: An array holding the above values.
    '''
    role = get_property(msgID, 1)
    data= [0,0,0,0,0,0,0,0,0]
    data[0] = role%16               # 4-bit Product Identifier
    data[1] = int(role/2**6)%2==1   # Internal Thermistor Bit
    data[2] = int(role/2**7)%2==1   # 20 MHz (vs 32 MHz)
    data[3] = int(role/2**8)%2==1   # Is there a Dig+Ser Motor Encoder?
    data[4] = int(role/2**9)%2==1   # Is there a Hall Motor Encoder?
    data[5] = int(role/2**10)%2==1  # Is there an Enc Motor Encoder?
    data[6] = int(role/2**11)%2==1  # Is there a Strain Gauge?
    data[7] = int(role/2**12)%2==1  # IMU for Force-Torque Sensor
    data[8] = int(role/2**13)%2==1  # Optical Motor Encoder
    return data

def get_mode(msgID):
    '''
    Read from MODE property, and return a tuple with the number corresponding to the mode, along with
    the string name of the mode.

        @param msgID: The puck from which to get the mode.
        @type msgID: int
        @rtype: Tuple(int, str)
        @return: A tuple with the number and name of the mode.
    '''
    m = get_property(msgID, MODE)
    if m==MODE_IDLE:
        return (MODE_IDLE, "IDLE")
    elif m==MODE_TORQUE:
        return (MODE_TORQUE, "TORQUE")
    elif m==MODE_PID:
        return (MODE_PID, "PID")
    elif m==MODE_VEL:
        return (MODE_VEL, "VEL")
    elif m==MODE_TRAP:
        return (MODE_TRAP, "TRAP")
    else:
        print "Invalid get_mode() operation: "+str(m)
        return (m, "???")

def set_mode(msgID, value):
    '''
    Set the mode property using either strings or numbers.

        @param msgID: The puck or group to set the mode.
        @type msgID: int
        @param value: The value to which the mode should be set.
        @type value: int
    '''
    modes = {"IDLE":MODE_IDLE, "TORQUE":MODE_TORQUE, "PID":MODE_PID, "VEL":MODE_VEL, "TRAP":MODE_TRAP}
    m = value
    if m in modes:
        m = modes[m]
    set_property(msgID, MODE, m)
    
# I'm sorry that this method is so unbearably long, but it won't compile otherwise because of circular imports TT_TT
def set_puck_like(puckID, virtID):
    '''
    Set the puck to have all the default properties of the indicated puck ID.

        @param puckID: The original puck to change.
        @type puckID: int
        @param virtID: The ID of the puck to load defaults from.
        @type virtID: int
    '''
    set_property(puckID, MODE, MODE_IDLE)
    # Set universal puck properties. (taterDefs[])
    # if virtID in range(1,8)
    #     set_property(puckID, TIE, 0)
    #     set_property(puckID, ACCEL, 100)
    #     set_property(puckID, AP, 0)
    #     set_property(puckID, CT, 4096)
    #     set_property(puckID, OT, 0)
    #     set_property(puckID, CTS, 4096)
    #     set_property(puckID, DP, 0)
    #     set_property(puckID, MV, 100)
    #     set_property(puckID, MCV, 100)
    #     set_property(puckID, MOV, 100)
    #     set_property(puckID, OT, 0)
    #     set_property(puckID, HOLD, 0)
    #     set_property(puckID, TSTOP, 0)
    #     set_property(puckID, OTEMP, 60)
    #     set_property(puckID, PTEMP, 0)
    #     set_property(puckID, DS, -256)
    #     set_property(puckID, KP, 2000)
    #     set_property(puckID, KD, 8000)
    #     set_property(puckID, KI, 0)
        #wamDefaultMT has yet to be implemented correctly. The interns coding this don't really care about the WAM, so this will be put off until someone does.
    
    #Set Barrett Hand Defaults
    is_280 = get_property(puckID, HALLH)==7 #Identifier for 280 version
    if virtID in [FINGER1, FINGER2, FINGER3, SPREAD]:
        set_property(puckID, JIDX, virtID-3)
        save_property(puckID, JIDX)
        set_property(puckID, PIDX, virtID-10)
        save_property(puckID, PIDX)
        set_property(puckID, TIE, 0)
        save_property(puckID, TIE)
        set_property(puckID, ACCEL, 200)
        save_property(puckID, ACCEL)
        #set_property(puckID, AP, 0)
        #save_property(puckID, AP)
        set_property(puckID, OT, 0)
        save_property(puckID, OT)
        set_property(puckID, CTS, 4096)
        save_property(puckID, CTS)
        set_property(puckID, MT, 2200)
        save_property(puckID, MT)
        set_property(puckID, MCV, 200)
        save_property(puckID, MCV)
        set_property(puckID, MOV, 200)
        save_property(puckID, MOV)
        set_property(puckID, OTEMP, 60)
        save_property(puckID, OTEMP)
        set_property(puckID, PTEMP, 0)
        save_property(puckID, PTEMP)
        set_property(puckID, POLES, 6)
        save_property(puckID, POLES)
        set_property(puckID, IKCOR, 102)
        save_property(puckID, IKCOR)
        set_property(puckID, IOFF, 0)
        save_property(puckID, IOFF)
        set_property(puckID, IVEL, -75)
        save_property(puckID, IVEL)
        set_property(puckID, DS, 25600)
        save_property(puckID, DS)
        set_property(puckID, KI, 0)
        save_property(puckID, KI)
        set_property(puckID, IPNM, 20000)
        save_property(puckID, IPNM)
        set_property(puckID, GRPA, 0)
        save_property(puckID, GRPA)
        set_property(puckID, GRPB, 7)
        save_property(puckID, GRPB)
        set_property(puckID, GRPC, 5)
        save_property(puckID, GRPC)
        set_property(puckID, IKI, 204)
        save_property(puckID, IKI)
        set_property(puckID, IKP, 500)
        save_property(puckID, IKP)
        if virtID == SPREAD:
            set_property(puckID, CT, 35950)
            save_property(puckID, CT)
            set_property(puckID, DP, 17975)
            save_property(puckID, DP)
            set_property(puckID, MV, 50)
            save_property(puckID, MV)
            set_property(puckID, HSG, 0)
            save_property(puckID, HSG)
            set_property(puckID, LSG, 0)
            save_property(puckID, LSG)
            set_property(puckID, HOLD, 1)
            save_property(puckID, HOLD)
            set_property(puckID, TSTOP, 150)
            save_property(puckID, TSTOP)
            set_property(puckID, KP, 1000)
            save_property(puckID, KP)
            set_property(puckID, KD, 10000)
            save_property(puckID, KD)
        else:
            set_property(puckID, CT, 195000)
            save_property(puckID, CT)
            set_property(puckID, DP, 45000)
            save_property(puckID, DP)
            set_property(puckID, MV, 200)
            save_property(puckID, MV)
            set_property(puckID, HSG, 0)
            save_property(puckID, HSG)
            set_property(puckID, LSG, 0)
            save_property(puckID, LSG)
            set_property(puckID, HOLD, 0)
            save_property(puckID, HOLD)
            set_property(puckID, TSTOP, 50)
            save_property(puckID, TSTOP)
            set_property(puckID, KP, 500)
            save_property(puckID, KP)
            set_property(puckID, KD, 2500)
            save_property(puckID, KD)
    else:
        print "Invalid Puck Id for Hand"
    
#============================MOVING_STUFF================================

def set_hand_targets(f1_target, f2_target, f3_target, sp_target):
    '''
    Given fingers and spread target values, move the hand to that position.
    Will mainly be used to load user-defined hand positions.
    Takes Barrett Units as inputs.

        @param f1_target: The position (in encoder ticks) for finger 1 to move to.
        @type f1_target: int
        @param f2_target: The position for finger 2 to move to.
        @type f2_target: int
        @param f3_target: The position for finger 3 to move to.
        @type f3_target: int
        @param sp_target: The position for spread to move to.
        @type sp_target: int
    '''
    set_property(FINGER1, DP, f1_target)
    set_property(FINGER2, DP, f2_target)
    set_property(FINGER3, DP, f3_target)
    tar = get_position(SPREAD)
    set_property(SPREAD, DP, tar)
    set_property(0x405, CMD, CMD_MOVE)
    time.sleep(2)
    set_property(SPREAD, DP, sp_target)
    set_property(SPREAD, CMD, CMD_MOVE)
    time.sleep(1)

def move_to(puckID, target, autowait=True):
    '''
    Move the motor to a specific position.

        @param puckID: The puck to move.
        @type puckID: int
        @param target: The end position to move to.
        @type target: int
        @param autowait: Does the program wait until the motor is done moving?
        @type autowait: bool
    '''
    set_property(puckID, M, target)
    if autowait:
        wait_done_moving([puckID])

def done_moving(motors_to_check=ALL_FINGERS):
    '''
    Checks a given list of motors once to see if they have stopped moving, and if so, it returns true

        @param motors_to_check: A list of motors to check.
        @type motors_to_check: Array[*int]
        @rtype: bool
        @return: Whether or not the motors are done moving.
    '''
    for FINGER in motors_to_check:
        if (get_mode(FINGER)[1]!="IDLE" and (get_mode(FINGER)[1]!="PID" or get_property(FINGER,77)==0)):
            return False
    return True

# TODO: Ensure that TSTOP > 0. Otherwise, this may be an infinite loop.
def wait_done_moving(motors_to_check=ALL_FINGERS):
    '''
    Waits until the given list of motors have all stopped moving.

        @param motors_to_check: A list of motors to wait for.
        @type motors_to_check: Array[*int]
    '''
    while(not done_moving(motors_to_check)):
        time.sleep(0.025)

def detect_breakaway(finger):
    '''

        @return: True if the finger has broken away, False if it hasn't
    '''
    tup = get_packed_position(finger)
    ratio = tup[0]/tup[1]
    return (ratio>3)

def open_grasp():
    '''
    Opens all fingers to the position encoded by Open Target (OT)
    '''
    set_property(0x405, TSTOP, 50)
    set_property(SPREAD, TSTOP, 150)

    open_target=get_property(FINGER1,OT)
    set_property(FINGER1,DP,open_target)
    
    open_target=get_property(FINGER2,OT)
    set_property(FINGER2,DP,open_target)
    
    open_target=get_property(FINGER3,OT)
    set_property(FINGER3,DP,open_target)

    spread_stay=get_position(SPREAD)
    set_property(SPREAD,DP,spread_stay)
    
    set_property(0x405,CMD,CMD_MOVE)
    wait_done_moving(GRASP)

def close_grasp():
    '''
    Closes all fingers to the position encoded by Close Target (CT).
    '''
    set_property(0x405, TSTOP, 50)
    set_property(SPREAD, TSTOP, 150)

    close_target=get_property(FINGER1,CT)
    set_property(FINGER1,DP,close_target)

    close_target=get_property(FINGER2,CT)
    set_property(FINGER2,DP,close_target)

    close_target=get_property(FINGER3,CT)
    set_property(FINGER3,DP,close_target)

    spread_stay=get_position(SPREAD)
    set_property(SPREAD,DP,spread_stay)

    set_property(0x405,CMD,CMD_MOVE)
    wait_done_moving(GRASP)
    
def open_spread():
    '''
    Open spread to position determined by Open Target (OT).
    '''
    set_property(SPREAD, TSTOP, 150)
    set_property(SPREAD, CMD, CMD_OPEN)
    wait_done_moving([SPREAD])

def close_spread():
    '''
    Close spread to position determined by Close Target (CT).
    '''
    set_property(SPREAD, CMD, CMD_CLOSE)
    wait_done_moving([SPREAD])

def open_finger(puckID, autowait=True):
    '''
    Open finger and wait for completion.

        @param puckID: Finger to be opened.
        @type puckID: int
        @param autowait: calls wait_done_moving if True. Defaults to True.
        @type autowait: bool
    '''
    if puckID in [FINGER1, FINGER2, FINGER3]:
        set_property(puckID, TSTOP, 50)
    if puckID == SPREAD:
        set_property(puckID, TSTOP, 150)
    set_property(puckID, CMD, CMD_OPEN)
    if autowait:
        wait_done_moving([puckID])

def close_finger(puckID, autowait=True):
    '''
    Close finger and wait for completion.

    @param puckID: Finger to be closed.
    @type puckID: int
    @param autowait: calls wait_done_moving if True. Defaults to True.
    @type autowait: bool
    '''
    if puckID in [FINGER1, FINGER2, FINGER3]:
        set_property(puckID, TSTOP, 50)
    if puckID == SPREAD:
        set_property(puckID, TSTOP, 150)
    set_property(puckID, CMD, CMD_CLOSE)
    if autowait:
        wait_done_moving([puckID])

def move_grasp(position = -1):
    '''
    Moves all fingers to input argument or default position (50).

        @param position: position of fingers. Defaults to -1. Valid position range is from 0-195,000 encoder counts.
        @type position: int
    '''
    default = get_position(SPREAD)
    set_property(SPREAD, DP, default)
    if(position != -1):
    	set_property(FINGER1, DP, position)
    	set_property(FINGER2, DP, position)
    	set_property(FINGER3, DP, position)	
    move()

def move():
    '''
    Moves all fingers/spread to their default.
    '''
    set_property(0x405, CMD, CMD_MOVE)
    wait_done_moving(GRASP)

def open_all():
    '''
    Opens every fingers at once. Mainly used in DEMO. WARNING: can be dangerous because it may cause fingers to collide if the hand is in an unknown position.
    '''
    open_target = get_property(FINGER1, OT)
    set_property(FINGER1, DP, open_target)
    open_target = get_property(FINGER2, OT)
    set_property(FINGER2, DP, open_target)
    open_target = get_property(FINGER3, OT)
    set_property(FINGER3, DP, open_target)
    open_target = get_property(SPREAD, OT)
    set_property(SPREAD, DP, open_target)
    move()

def close_all():
    '''
    Closes every finger at once. Mainly for use in DEMO. WARNING: can be dangerous because it may cause fingers to collide if the hand is in an unknown position.
    '''
    close_target = get_property(FINGER1, CT)
    set_property(FINGER1, DP, close_target)
    close_target = get_property(FINGER2, CT)
    set_property(FINGER2, DP, close_target)
    close_target = get_property(FINGER3, CT)
    set_property(FINGER3, DP, close_target)
    close_target = get_property(SPREAD, CT)
    set_property(SPREAD, DP, close_target)
    move()

#============================INCREMENTALLY_MOVE_STUFF========================
    
def open_grasp_step(step=0):
    '''
    Open grasp by input increment.

        @param step: size of increment in encoder counts. Defaults to 0.
        @type step: int
    '''
    open_finger_step(FINGER1, step, False)
    open_finger_step(FINGER2, step, False)
    open_finger_step(FINGER3, step, False)
    wait_done_moving(GRASP)

def close_grasp_step(step=0):
    '''
    Close grasp by input decrement.

        @param step: size of decrement in encoder counts. Defaults to 0.
        @type step: int
    '''
    close_finger_step(FINGER1, step, False)
    close_finger_step(FINGER2, step, False)
    close_finger_step(FINGER3, step, False)
    wait_done_moving(GRASP)

def open_spread_step(step=-1):
    '''
    Open spread by input increment.

        @param step: size of increment in encoder counts. Defaults to -1.
        @type step: int
    '''
    if step == -1:
        step = get_property(SPREAD, 60)
    open_finger_step(SPREAD, step)
    
def close_spread_step(step=-1):
    '''
    Close spread by input decrement.

        @param step: size of decrement in encoder counts. Defaults to -1.
        @type step: int 
    '''
    if step == -1:
        step = get_property(SPREAD, 60)
    close_finger_step(SPREAD, step)

def open_finger_step(puckID, step=-1, autowait=True):
    '''
    Open finger by input increment.

        @param puckID: Finger to be opened.
        @type puckID: int
        @param step: size of increment in encoder counts. Defaults to -1.
        @type step: int
        @param autowait: calls wait_done_moving if True. Defaults to True.
        @type autowait: bool
    '''
    if step == -1:
        step = get_property(puckID, 60)
    set_property(puckID, DS, step)
    set_property(puckID, CMD, CMD_IO)
    if autowait:
        wait_done_moving([puckID])

def close_finger_step(puckID, step=-1, autowait=True):
    '''
    Close finger by input decrement.

        @param puckID: Finger to be closed.
        @type puckID: int
        @param step: size of decrement in encoder counts. Defaults to -1.
        @type step: int
        @param autowait: calls wait_done_moving if True. Defaults to True.
        @type autowait: bool
    '''
    if step == -1:
        step = get_property(puckID, 60)
    set_property(puckID, DS, step)
    set_property(puckID, CMD, CMD_IC)
    if autowait:
        wait_done_moving([puckID])

#===========================NON_TRIVIAL FUNCTIONS=============================

def get_velocity(msgID):
    '''
    Returns velocity values of finger when in motion. Mostly returns garbage. It's used to help tell when finger is stopped or near to it.

        @param msgID: The puck or group to get velocity.
        @type msgID: int
        @rtype: float
        @return: A (garbage) value representing the approximate velocity of the finger.
    '''    
    def get_full_pos_packet(msgID):
        write_msg(msgID, [P])
        read_result=PCAN.Read(PCAN_USBBUS1)
        return read_result
    
    packet1=get_full_pos_packet(msgID)
    packet2=get_full_pos_packet(msgID)
    
    error1=packet1[0]
    error2=packet2[0]

    msg1=packet1[1]
    msg2=packet2[1]

    data1=msg1.DATA 
    data2=msg2.DATA

    time1=packet1[2]
    time2=packet2[2]
    
    stamp1=time1.micros + 1000 * time1.millis + 0xFFFFFFFF * 1000 * time1.millis_overflow
    stamp2=time2.micros + 1000 * time2.millis + 0xFFFFFFFF * 1000 * time2.millis_overflow

    delta=(stamp2-stamp1)/1000000.0
    
    check_error(PCAN,error1,"reading position for fake get_velocity")
    check_error(PCAN,error2,"reading position for fake get_velocity")

    val1=(0x0000100 * data1[3]) + (0x0000001 * data1[2])
    val2=(0x0000100 * data2[3]) + (0x0000001 * data2[2])
    
    return (val2-val1)/delta

def get_temp(msgID):
    '''
    Gets temperature value for all pucks in msgID.

        @param msgID: The puck or group to get temp.
        @type msgID: int
        @rtype: int
        @return: The value of the TEMP property.
    '''
    return get_property(msgID, TEMP)

def get_therm(msgID):
    '''
    Gets motor temperature value for all pucks in msgID. 

        @param msgID: The puck or group to get motor temperature.
        @text msgID: int
        @rtype: int
        @return: The value of the THERM property.
    '''
    return get_property(msgID, THERM)

def get_top_tact(msgID):
    '''
    Unpack the top10 values from TACT.
    Returns a dictionary with 10 items like (sensor number):(tact value).

        @param msgID: The puck or group to get top 10 tactile data.
        @type msgID: int
        @rtype: Dictionary{sensorID:value}
        @return topVals: Dictionary of the top 10 tactile array sensor values. 
    '''
    # Set TACT(106) to top10 mode (1)
    set_property(msgID, TACT, TACT_10) 
    write_msg(msgID, [TACT]) #GET TACT
    global PCAN
    read_result=PCAN.Read(PCAN_USBBUS1)
    check_error(PCAN,read_result[0],"reading top ten tactile values")
    #output is mapped to here.
    output = read_result[1].DATA 
    #parsing this output
    top10 = output[0] * 0x10000 + output[1] * 0x100 + output[2] * 0x1
    topVals = {}
    data = [output[3]/(0x10), output[3]%(0x10), output[4]/(0x10), output[4]%(0x10), output[5]/(0x10), output[5]%(0x10)]
    count=0
    for sensor in range(0, 24):
        if top10%2 == 1:
            topVals[sensor] = data[count]
            count+=1
        top10 = top10/2
        # Each bit represents one of the top 10 pressures for purposes of efficiency. top10 has the last bit sliced
    return topVals

def get_full_tact(msgID):
    '''
    Unpack all tactile sensor values in an array.

        @param msgID: The puck or group to get full tactile array sensor data.
        @type msgID: int
        @rtype: Array[*data]
        @return: An array containing the tactile data from a given puck.
    '''
    global PCAN
    # Set TACT(106) to full mode (2)
    set_property(msgID, TACT, TACT_FULL) 
    write_msg(msgID, [TACT])
    output = [0,0,0,0,0]
    read_result = PCAN.Read(PCAN_USBBUS1)
    check_error(PCAN,read_result[0],"reading full tactile data")
    read_result2 = PCAN.Read(PCAN_USBBUS1)
    check_error(PCAN,read_result2[0],"reading full tactile data")
    read_result3 = PCAN.Read(PCAN_USBBUS1)
    check_error(PCAN,read_result3[0],"reading full tactile data")
    read_result4 = PCAN.Read(PCAN_USBBUS1)
    check_error(PCAN,read_result4[0],"reading full tactile data")
    read_result5 = PCAN.Read(PCAN_USBBUS1)
    check_error(PCAN,read_result5[0],"reading full tactile data")
    
    output[0] = read_result[1].DATA
    output[1] = read_result2[1].DATA
    output[2] = read_result3[1].DATA
    output[3] = read_result4[1].DATA
    output[4] = read_result5[1].DATA
    
    tactileVals = range(0,24)
    index = 0
    for data in output:
        index = int(data[0]/16) * 5
        # Get the bits and then unpack them.
        tactileVals[index + 0] = round(((data[0]%0x10)*0x100 + data[1])/256.0,2)
        tactileVals[index + 1] = round((data[2]*0x10 + int(data[3]/0x10))/256.0,2)
        tactileVals[index + 2] = round(((data[3]%0x10)*0x100 + data[4])/256.0,2)
        tactileVals[index + 3] = round((data[5]*0x10 + int(data[6]/0x10))/256.0,2)
        if index != 20:
            tactileVals[index + 4] = round(((data[6]%0x10)*0x100 + data[7])/256.0,2)
    return tactileVals

def get_tact(msgID, topOrFull="TOP10"):
    '''
    Obtain and interpret tactile sensor data.

        @param msgID: The puck or group to get full or top 10 tactile array sensor data.
        @type msgID: int
        @param topOrFull: To get full data, enter "FULL". To get the top 10 values, enter "TOP10". Or anything else, really.
        @type topOrFull: str
        @return 
    '''
    if topOrFull == "FULL":
        return get_full_tact(msgID)
    else:
        return get_top_tact(msgID)

def set_velocity(puckID, velocity):
    '''
    Set the velocity and make the motor move.

        @param puckID: The ID of the puck to set the velocity of.
        @type puckID: int
        @param velocity: The velocity (in cts/ms) of the motor.
        @type velocity: int
    '''
    #First set TSTOP to 0.
    set_property(puckID, TSTOP, 0)
    #Set Velocity
    set_property(puckID, V, velocity)
    #Set mode to allow the puck to move.
    set_property(puckID, MODE, MODE_VEL)

def get_strain(msgID):
    '''
    Gets the fingertip torque sensor value. 

        @param msgID: The puck or group to get fingertip torque sensor data. 
        @type msgID: int
        @rtype: int
        @return: Strain Gauge Reading
    '''
    return get_property(msgID, SG)

def onescomp(binstr):
    return ''.join('1' if b=='0' else '0' for b in binstr)

def twoscomp(number, bits):
    '''
    Returns the two's complement of a number with a certain amount of bits.

        @param number: The number to take the two's complement of.
        @type number: int
        @param bits: The size of the integer in bits.
        @type bits: int
    '''
    return -(1<<bits) + number

def get_position(msgID, depth=0):
    '''
    Get packed position data and return it.

        @param msgID: The puck or group to get position data.
        @type msgID: int
        @rtype: int

        @param depth: number of times get message was retried.
        
        @return: The position of the finger in encoder counts.
    '''
    if depth!=0:
        write_msg(msgID, [P],.009)
    read_result=PCAN.Read(PCAN_USBBUS1)
    try:
        check_error(PCAN,read_result[0],"getting position data")
        received_puck=(read_result[1].ID-1024)>>5
        if received_puck!=msgID:
            raise Exception("Did not read expected MSGID")
    except:
        if depth>10:
            raise Exception("Failure to get position data.")
        else:
            return get_position(msgID, depth+1)

    output = read_result[1].DATA
    temp=(output[0]-0x80)*0x10000 + output[1] * 0x100 + output[2]

    if (temp & 2**21): 
        return twoscomp(temp & 0x3FFFFF, 22)
    else:
        return temp

def get_packed_position(msgID, depth=0):
    '''
    Get packed position data and return both P and JP.

        @param msgID: The puck or group to get position data.
        @type msgID: int
        @rtype: (int, int)

        @param depth: number of times get message was retried.

        @return: The position and joint position of the finger in encoder counts.
    '''
    #if depth==0:
        #write_msg(msgID, [P], .009)
    write_msg(msgID, [P], .009)
    read_in = read_msg()
    try:
        check_error(PCAN, read_in[0], "getting packed position data")
        received_puck=(read_in[1].ID-1024)>>5
        if received_puck!=msgID:
            raise Exception("Did not read expected MSGID")
    except:
        if depth>10:
            raise Exception("Failure to get packed position data.")
        else:
            return get_packed_position(msgID)
    data = read_in[1].DATA
    pos = (data[0]-0x80)*0x10000 + data[1]*0x100 + data[2]
    jpos= (data[3]-0x80)*0x10000 + data[4]*0x100 + data[5]
    pos = twoscomp(pos  & 0x1FFFFF,21) if pos  & 2**21 else pos
    jpos= twoscomp(jpos & 0x1FFFFF,21) if jpos & 2**21 else jpos
    return (pos, jpos)
    can_reset()

def new_temp_mail(fingers_to_change):
    former_mailbox_c={}
    for finger in fingers_to_change:
        former_mailbox_c[finger]=get_property(finger,GRPC)
        set_property(finger,GRPC,12)
    return former_mailbox_c

def revert_temp_mail(fingers_to_change,former):
    for finger in fingers_to_change:
        former_mailbox_value=former[finger]
        set_property(finger,GRPC,former_mailbox_value)
#==========================ANGLE_CONVERSIONS=========================

def enc_to_per(enc):
    '''
    Given an angle in encoder counts, return the percentage of the angle that represents.

        @param enc: Encoder counts.
        @type enc: int
        @return: Percentage
        @rtype: float
    '''
    per = enc/1950.0
    return round(per, 2)

def enc_to_rad(enc):
    '''
    Given an angle in encoder counts, return the radian measure of the angle that represents.

        @param enc: Encoder counts.
        @type enc: int
        @return: Radians
        @rtype: float
    '''
    PI = 3.141592653589
    rad = enc * (140*PI/180)/195000.0
    return round(rad,2)

def enc_to_deg(enc):
    '''
    Given an angle in encoder counts, return the degree measure of the angle that represents.

        @param enc: Encoder counts.
        @type enc: int
        @return: Degrees
        @rtype: float
    '''
    deg = enc * 140/195000.0
    return round(deg,2)

def per_to_enc(per):
    '''
    Given a percentage of an angle, return it in encoder counts.

        @param per: Percentage
        @type per: float
        @return: Encoder counts
        @rtype: int
    '''
    enc = per * 1950.0
    return int(enc)

def rad_to_enc(rad):
    '''
    Given the readian measure of an angle, return it in encoder counts.

        @param rad: Radians
        @type rad: float
        @return: Encoder counts
        @rtype: int
    '''
    PI = 3.141592653589
    enc = rad / ((140*PI/180)/195000.0)
    return int(enc)

def deg_to_enc(deg):

    '''
    Given a degree measure of an angle, return it in encoder counts.

        @param deg: Degrees
        @type deg: float
        @return: Encoder counts
        @rtype: int
    '''
    enc = deg * 195000.0/140
    return int(enc)
